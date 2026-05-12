"""
ingest.py — One-shot pipeline:
  1. Create Supabase tables (jobs, courses, students)
  2. Seed jobs from data/jobs.csv
  3. Seed courses from data/courses_catalog.csv
  4. Insert fake students
  5. Create Weaviate collections (Job, Course)
  6. Embed jobs → Weaviate Job collection (hybrid: BM25 + semantic)
  7. Embed courses → Weaviate Course collection

Run:
  python ingest.py

Prerequisites:
  - docker run -d --name weaviate -p 8080:8080 -p 50051:50051
      -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
      -e DEFAULT_VECTORIZER_MODULE=none
      -e ENABLE_MODULES=""
      cr.weaviate.io/semitechnologies/weaviate:1.25.4
  - ollama pull nomic-embed-text
  - .env filled with SUPABASE_URL + SUPABASE_KEY + WEAVIATE_URL
"""

import csv
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Repo root `.env` (SUPABASE_URL, SUPABASE_KEY, etc.) — load before db imports
REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

import sys
sys.path.insert(0, str(REPO_ROOT / "weaviate"))

from db.supabase_client import get_supabase
from db.weaviate_client import get_weaviate
from retrieval.job_content import extract_job_skills
from retrieval.record_utils import course_skills_value, job_skills_value
from retrieval.skills import extract_skill_names

# CSV/SQL live at repo root `data/` (not under `server/`)
DATA_DIR = REPO_ROOT / "data"
JOBS_CSV = DATA_DIR / "jobs.csv"
COURSES_CSV = DATA_DIR / "courses_catalog.csv"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_course_skills(raw: str) -> list[str]:
    """
    Parse course skills string like:
      [(Java, 45), (Programming Fundamentals, 35), (Problem Solving, 20)]
    into: [{"skill": "Java", "weight": 45}, ...]
    """
    # Non-greedy .+? correctly handles skill names that contain commas or
    # nested parentheses, e.g. "CNN Architectures (ResNet, VGG), 17".
    pattern = re.findall(r"\((.+?),\s*(\d+)\)", raw)
    return [s.strip() for s, _ in pattern if s.strip() and not s.strip().isdigit()]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def detect_schema_layout() -> dict[str, str]:
    sb = get_supabase()

    def detect(table: str, preferred: str, fallback: str, probe: str) -> str:
        try:
            sb.table(table).select(preferred).limit(1).execute()
            return preferred
        except Exception:
            sb.table(table).select(fallback).limit(1).execute()
            return fallback

    return {
        "jobs_skills": detect("jobs", "skills_jobs", "skills_jobs_json", "job_id"),
        "courses_skills": detect("courses", "skills_courses", "skills_courses_json", "course_id"),
        "students_completed": detect("students", "completed_courses", "completed_courses_json", "student_id"),
        "students_profile": detect("students", "skill_profile", "skill_profile_json", "student_id"),
        "students_recommendations": detect("students", "last_recommendations", "last_recommendations_json", "student_id"),
    }


SCHEMA_LAYOUT = detect_schema_layout()


def clear_existing_data():
    print("\n[reset] Clearing existing Supabase rows and Weaviate collections...")
    sb = get_supabase()
    nil_uuid = "00000000-0000-0000-0000-000000000000"
    sb.table("jobs").delete().neq("job_id", nil_uuid).execute()
    sb.table("courses").delete().neq("course_id", nil_uuid).execute()
    sb.table("students").delete().neq("student_id", nil_uuid).execute()

    client = get_weaviate()
    for class_name in ["Job", "Course"]:
        if client.collections.exists(class_name):
            client.collections.delete(class_name)
            print(f"  Deleted collection: {class_name}")
    print("  Cleared jobs, courses, students.")


# ---------------------------------------------------------------------------
# Step 1: Create tables
# ---------------------------------------------------------------------------

def create_tables():
    print("\n[1/7] Creating Supabase tables...")
    sb = get_supabase()

    schema_path = DATA_DIR / "schema.sql"
    sql = schema_path.read_text()

    # Supabase JS client doesn't expose raw SQL — use rpc or just note tables
    # must be created manually via Supabase dashboard SQL editor.
    # We'll verify by attempting a select and catching errors.
    try:
        sb.table("jobs").select("job_id").limit(1).execute()
        sb.table("courses").select("course_id").limit(1).execute()
        sb.table("students").select("student_id").limit(1).execute()
        print("  Tables already exist.")
    except Exception:
        print("  WARNING: Tables may not exist yet.")
        print("  Please run data/schema.sql in the Supabase SQL editor, then re-run this script.")
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# Step 2: Seed jobs
# ---------------------------------------------------------------------------

def seed_jobs() -> list[dict]:
    print("\n[2/7] Seeding jobs from jobs.csv...")
    sb = get_supabase()
    skills_field = SCHEMA_LAYOUT["jobs_skills"]

    rows = []
    with open(JOBS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            job_id = row.get("job_id") or str(uuid.uuid4())
            title = row.get("title", "").strip()
            description = row.get("job_description_raw", "").strip()
            precomputed = row.get("skills", "").strip()
            parsed_skills = extract_job_skills(title, description, precomputed=precomputed)
            job_record = {
                "job_id": job_id,
                "source": row.get("source", ""),
                "title": title,
                "company": row.get("company", "").strip(),
                "location": row.get("location", "").strip(),
                "description": description,
                "posted_at": None,
                "ingested_at": now_iso(),
            }
            job_record[skills_field] = parsed_skills
            rows.append({
                **job_record
            })

    # Upsert in batches of 100
    batch_size = 100
    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        sb.table("jobs").upsert(batch, on_conflict="job_id").execute()
        print(f"  Upserted jobs {i + 1}–{min(i + batch_size, len(rows))}")

    # Ensure skills arrays are persisted reliably for every row.
    # (Some Supabase setups can drop array fields during large upsert batches.)
    for row in rows:
        sb.table("jobs").update(
            {skills_field: row[skills_field]}
        ).eq("job_id", row["job_id"]).execute()

    print(f"  Total jobs seeded: {len(rows)}")
    return rows


# ---------------------------------------------------------------------------
# Step 3: Seed courses
# ---------------------------------------------------------------------------

def seed_courses() -> list[dict]:
    print("\n[3/7] Seeding courses from courses_catalog.csv...")
    sb = get_supabase()
    skills_field = SCHEMA_LAYOUT["courses_skills"]
    existing_rows = sb.table("courses").select("course_id,course_code").execute().data
    existing_ids = {
        (row.get("course_code") or "").strip(): row.get("course_id")
        for row in existing_rows
        if row.get("course_code") and row.get("course_id")
    }

    rows = []
    with open(COURSES_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            course_code = row.get("course_code", "").strip()
            course_id = existing_ids.get(course_code) or str(uuid.uuid4())
            skills = parse_course_skills(row.get("skills", ""))
            course_record = {
                "course_id": course_id,
                "course_code": course_code,
                "title": row.get("title", "").strip(),
                "description": row.get("description", "").strip(),
                "updated_at": now_iso(),
            }
            course_record[skills_field] = skills
            rows.append({
                **course_record
            })

    sb.table("courses").upsert(rows, on_conflict="course_code").execute()
    print(f"  Total courses seeded: {len(rows)}")
    return rows


# ---------------------------------------------------------------------------
# Step 4: Insert fake students
# ---------------------------------------------------------------------------

FAKE_STUDENTS = [
    {
        "student_id": "00000000-0000-0000-0000-000000000001",
        "name": "Alex Chen",
        "major": "Computer Science",
        "completed_courses": ["CSC 101", "CSC 220", "CSC 315", "CSC 340"],
        "skill_profile": ["Python", "Java", "Data Structures", "Algorithms", "Object-Oriented Programming"],
        "last_recommendations": None,
        "updated_at": now_iso(),
    },
    {
        "student_id": "00000000-0000-0000-0000-000000000002",
        "name": "Maria Gomez",
        "major": "Computer Science",
        "completed_courses": ["CSC 220", "CSC 415", "CSC 510", "CSC 600", "CSC 667"],
        "skill_profile": ["Machine Learning", "Python", "Databases", "Operating Systems", "Deep Learning", "SQL"],
        "last_recommendations": None,
        "updated_at": now_iso(),
    },
    {
        "student_id": "00000000-0000-0000-0000-000000000003",
        "name": "Sam Patel",
        "major": "Computer Science",
        "completed_courses": ["CSC 101", "CSC 110", "CSC 215"],
        "skill_profile": ["Java", "Programming Fundamentals", "Computational Thinking", "Problem Solving"],
        "last_recommendations": None,
        "updated_at": now_iso(),
    },
]


def seed_students():
    print("\n[4/7] Inserting fake students...")
    sb = get_supabase()
    student_rows = []
    for student in FAKE_STUDENTS:
        row = {
            "student_id": student["student_id"],
            "name": student["name"],
            "major": student["major"],
            "updated_at": student["updated_at"],
        }
        row[SCHEMA_LAYOUT["students_completed"]] = student["completed_courses"]
        row[SCHEMA_LAYOUT["students_profile"]] = student["skill_profile"]
        row[SCHEMA_LAYOUT["students_recommendations"]] = student["last_recommendations"]
        student_rows.append(row)
    sb.table("students").upsert(student_rows, on_conflict="student_id").execute()
    for s in FAKE_STUDENTS:
        print(f"  Upserted: {s['name']} ({s['student_id']})")


# ---------------------------------------------------------------------------
# Step 5: Create Weaviate collections
# ---------------------------------------------------------------------------

def create_weaviate_collections():
    # Import here to avoid circular import issues with sys.path manipulation
    from index_jobs import recreate_collection as recreate_job_collection
    from index_courses import recreate_collection as recreate_course_collection

    print("\n[5/7] Creating Weaviate collections...")
    recreate_job_collection()
    print("  Created collection: Job")
    recreate_course_collection()
    print("  Created collection: Course")


# ---------------------------------------------------------------------------
# Step 6: Embed jobs → Weaviate
# ---------------------------------------------------------------------------

def embed_jobs(job_rows: list[dict]):
    from index_jobs import index_jobs as weaviate_index_jobs

    print(f"\n[6/7] Indexing {len(job_rows)} jobs into Weaviate (hybrid: BM25 + semantic)...")
    chunk_count = weaviate_index_jobs(job_rows)
    print(f"  Done. {chunk_count} chunk objects stored.")


# ---------------------------------------------------------------------------
# Step 7: Embed courses → Weaviate
# ---------------------------------------------------------------------------

def embed_courses(course_rows: list[dict]):
    from index_courses import index_courses as weaviate_index_courses

    print(f"\n[7/7] Indexing {len(course_rows)} courses into Weaviate (hybrid: BM25 + semantic)...")
    chunk_count = weaviate_index_courses(course_rows)
    print(f"  Done. {chunk_count} chunk objects stored.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weaviate-only",
        action="store_true",
        help="Skip Supabase seeding; only create Weaviate collections and embed.",
    )
    parser.add_argument(
        "--courses-only",
        action="store_true",
        help="Only sync course rows to Supabase.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete all rows from jobs/courses/students and recreate Qdrant collections before ingesting.",
    )
    args = parser.parse_args()

    if args.weaviate_only and args.courses_only:
        parser.error("--weaviate-only and --courses-only cannot be used together.")

    print("=" * 60)
    print("  Ingest Pipeline")
    print("=" * 60)

    should_print_complete = False

    if args.courses_only:
        create_tables()
        if args.reset:
            clear_existing_data()
        course_rows = seed_courses()
        print("\n" + "=" * 60)
        print(f"  Course sync complete. {len(course_rows)} rows updated.")
        print("=" * 60)
    elif not args.weaviate_only:
        create_tables()
        if args.reset:
            clear_existing_data()
        job_rows = seed_jobs()
        course_rows = seed_courses()
        seed_students()
        create_weaviate_collections()
        embed_jobs(job_rows)
        embed_courses(course_rows)
        should_print_complete = True
    else:
        print("\n[1-4/7] Skipping Supabase seeding (--weaviate-only).")
        print("        Fetching existing rows from Supabase...")
        sb = get_supabase()
        job_rows = [
            {
                "job_id": r["job_id"],
                "title": r["title"],
                "company": r["company"],
                "location": r.get("location", ""),
                "description": r.get("description", ""),
                SCHEMA_LAYOUT["jobs_skills"]: r.get(SCHEMA_LAYOUT["jobs_skills"]) or [],
            }
            for r in sb.table("jobs").select(f"job_id,title,company,location,description,{SCHEMA_LAYOUT['jobs_skills']}").execute().data
        ]
        course_rows = [
            {
                "course_id": r["course_id"],
                "course_code": r["course_code"],
                "title": r["title"],
                "description": r.get("description", ""),
                SCHEMA_LAYOUT["courses_skills"]: r.get(SCHEMA_LAYOUT["courses_skills"]) or [],
            }
            for r in sb.table("courses").select(f"course_id,course_code,title,description,{SCHEMA_LAYOUT['courses_skills']}").execute().data
        ]
        print(f"        Loaded {len(job_rows)} jobs, {len(course_rows)} courses.")

        create_weaviate_collections()
        embed_jobs(job_rows)
        embed_courses(course_rows)
        should_print_complete = True

    if should_print_complete:
        print("\n" + "=" * 60)
        print("  Ingest complete.")
        print("=" * 60)
