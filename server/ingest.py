"""
ingest.py — One-shot pipeline:
  1. Create Supabase tables (jobs, courses, students)
  2. Seed jobs from data/jobs.csv
  3. Seed courses from data/sfsu_csc_courses_clean_skills.csv
  4. Insert 3 fake students
  5. Create Qdrant collections
  6. Embed jobs → Qdrant jobs_collection
  7. Embed courses → Qdrant courses_collection

Run:
  python ingest.py

Prerequisites:
  - docker run -p 6333:6333 qdrant/qdrant
  - ollama pull nomic-embed-text
  - .env filled with SUPABASE_URL + SUPABASE_KEY
"""

import csv
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from db.supabase_client import get_supabase
from db.qdrant_client import get_qdrant
from retrieval.embedder import embed

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"
JOBS_CSV = DATA_DIR / "jobs.csv"
COURSES_CSV = DATA_DIR / "sfsu_csc_courses_clean_skills.csv"

JOBS_COLLECTION = "jobs_collection"
COURSES_COLLECTION = "courses_collection"
VECTOR_SIZE = 768  # nomic-embed-text output dimension

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_course_skills(raw: str) -> list[dict]:
    """
    Parse course skills string like:
      [(Java, 45), (Programming Fundamentals, 35), (Problem Solving, 20)]
    into: [{"skill": "Java", "weight": 45}, ...]
    """
    pattern = re.findall(r"\(([^,)]+),\s*(\d+)\)", raw)
    return [{"skill": s.strip(), "weight": int(w)} for s, w in pattern]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Step 1: Create tables
# ---------------------------------------------------------------------------

def create_tables():
    print("\n[1/7] Creating Supabase tables...")
    sb = get_supabase()

    schema_path = DATA_DIR / "JobSkill.sql"
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
        print("  Please run data/JobSkill.sql in the Supabase SQL editor, then re-run this script.")
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# Step 2: Seed jobs
# ---------------------------------------------------------------------------

def seed_jobs() -> list[dict]:
    print("\n[2/7] Seeding jobs from jobs.csv...")
    sb = get_supabase()

    rows = []
    with open(JOBS_CSV, newline="", encoding="utf-8") as f:
        # First line is "jobs" (artifact) — skip it
        first = f.readline().strip()
        if first != "jobs":
            f.seek(0)  # not an artifact, rewind
        reader = csv.DictReader(f)
        for row in reader:
            job_id = row.get("job_id") or str(uuid.uuid4())
            description = row.get("job_description_raw", "").strip()
            rows.append({
                "job_id": job_id,
                "source": row.get("source", ""),
                "title": row.get("title", "").strip(),
                "company": row.get("company", "").strip(),
                "location": row.get("location", "").strip(),
                "description": description,
                "skills_jobs_json": None,  # populated later if needed
                "posted_at": None,
                "ingested_at": now_iso(),
            })

    # Upsert in batches of 100
    batch_size = 100
    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        sb.table("jobs").upsert(batch, on_conflict="job_id").execute()
        print(f"  Upserted jobs {i + 1}–{min(i + batch_size, len(rows))}")

    print(f"  Total jobs seeded: {len(rows)}")
    return rows


# ---------------------------------------------------------------------------
# Step 3: Seed courses
# ---------------------------------------------------------------------------

def seed_courses() -> list[dict]:
    print("\n[3/7] Seeding courses from sfsu_csc_courses_clean_skills.csv...")
    sb = get_supabase()

    rows = []
    with open(COURSES_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            course_id = str(uuid.uuid4())
            skills = parse_course_skills(row.get("skills", ""))
            rows.append({
                "course_id": course_id,
                "course_code": row.get("course_code", "").strip(),
                "title": row.get("title", "").strip(),
                "description": row.get("description", "").strip(),
                "skills_courses_json": skills,
                "updated_at": now_iso(),
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
        "completed_courses_json": ["CSC 101", "CSC 220", "CSC 315", "CSC 340"],
        "skill_profile_json": [
            {"skill": "Python", "weight": 80},
            {"skill": "Java", "weight": 70},
            {"skill": "Data Structures", "weight": 65},
            {"skill": "Algorithms", "weight": 60},
            {"skill": "Object-Oriented Programming", "weight": 55},
        ],
        "last_recommendations_json": None,
        "updated_at": now_iso(),
    },
    {
        "student_id": "00000000-0000-0000-0000-000000000002",
        "name": "Maria Gomez",
        "major": "Computer Science",
        "completed_courses_json": ["CSC 220", "CSC 415", "CSC 510", "CSC 600", "CSC 667"],
        "skill_profile_json": [
            {"skill": "Machine Learning", "weight": 85},
            {"skill": "Python", "weight": 90},
            {"skill": "Databases", "weight": 70},
            {"skill": "Operating Systems", "weight": 60},
            {"skill": "Deep Learning", "weight": 75},
            {"skill": "SQL", "weight": 65},
        ],
        "last_recommendations_json": None,
        "updated_at": now_iso(),
    },
    {
        "student_id": "00000000-0000-0000-0000-000000000003",
        "name": "Sam Patel",
        "major": "Computer Science",
        "completed_courses_json": ["CSC 101", "CSC 110", "CSC 215"],
        "skill_profile_json": [
            {"skill": "Java", "weight": 50},
            {"skill": "Programming Fundamentals", "weight": 60},
            {"skill": "Computational Thinking", "weight": 45},
            {"skill": "Problem Solving", "weight": 55},
        ],
        "last_recommendations_json": None,
        "updated_at": now_iso(),
    },
]


def seed_students():
    print("\n[4/7] Inserting fake students...")
    sb = get_supabase()
    sb.table("students").upsert(FAKE_STUDENTS, on_conflict="student_id").execute()
    for s in FAKE_STUDENTS:
        print(f"  Upserted: {s['name']} ({s['student_id']})")


# ---------------------------------------------------------------------------
# Step 5: Create Qdrant collections
# ---------------------------------------------------------------------------

def create_qdrant_collections():
    print("\n[5/7] Creating Qdrant collections...")
    client = get_qdrant()

    for name in [JOBS_COLLECTION, COURSES_COLLECTION]:
        existing = [c.name for c in client.get_collections().collections]
        if name in existing:
            print(f"  Collection '{name}' already exists — skipping.")
        else:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
            print(f"  Created collection: {name}")


# ---------------------------------------------------------------------------
# Step 6: Embed jobs → Qdrant
# ---------------------------------------------------------------------------

def embed_jobs(job_rows: list[dict]):
    print(f"\n[6/7] Embedding {len(job_rows)} jobs into Qdrant...")
    client = get_qdrant()
    points = []

    for i, job in enumerate(job_rows):
        text = f"{job['title']} {job['company']} {job['description'][:500]}"
        vector = embed(text)
        points.append(
            PointStruct(
                id=str(uuid.UUID(job["job_id"])),
                vector=vector,
                payload={
                    "job_id": job["job_id"],
                    "title": job["title"],
                    "company": job["company"],
                    "skills": [],
                },
            )
        )
        if (i + 1) % 50 == 0:
            print(f"  Embedded {i + 1}/{len(job_rows)} jobs...")

    # Upsert in batches
    batch_size = 50
    for i in range(0, len(points), batch_size):
        client.upsert(collection_name=JOBS_COLLECTION, points=points[i : i + batch_size])

    print(f"  Done. {len(points)} job vectors stored.")


# ---------------------------------------------------------------------------
# Step 7: Embed courses → Qdrant
# ---------------------------------------------------------------------------

def embed_courses(course_rows: list[dict]):
    print(f"\n[7/7] Embedding {len(course_rows)} courses into Qdrant...")
    client = get_qdrant()
    points = []

    for course in course_rows:
        skills_text = " ".join(
            s["skill"] for s in (course.get("skills_courses_json") or [])
        )
        text = f"{course['course_code']} {course['title']} {course['description']} {skills_text}"
        vector = embed(text)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "course_id": course["course_id"],
                    "course_code": course["course_code"],
                    "title": course["title"],
                    "skills": [s["skill"] for s in (course.get("skills_courses_json") or [])],
                },
            )
        )

    client.upsert(collection_name=COURSES_COLLECTION, points=points)
    print(f"  Done. {len(points)} course vectors stored.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--qdrant-only",
        action="store_true",
        help="Skip Supabase seeding; only create Qdrant collections and embed.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Ingest Pipeline")
    print("=" * 60)

    if not args.qdrant_only:
        create_tables()
        job_rows = seed_jobs()
        course_rows = seed_courses()
        seed_students()
    else:
        print("\n[1-4/7] Skipping Supabase seeding (--qdrant-only).")
        print("        Fetching existing rows from Supabase...")
        sb = get_supabase()
        job_rows = [
            {
                "job_id": r["job_id"],
                "title": r["title"],
                "company": r["company"],
                "description": r.get("description", ""),
            }
            for r in sb.table("jobs").select("job_id,title,company,description").execute().data
        ]
        course_rows = [
            {
                "course_id": r["course_id"],
                "course_code": r["course_code"],
                "title": r["title"],
                "description": r.get("description", ""),
                "skills_courses_json": r.get("skills_courses_json") or [],
            }
            for r in sb.table("courses").select("*").execute().data
        ]
        print(f"        Loaded {len(job_rows)} jobs, {len(course_rows)} courses.")

    create_qdrant_collections()
    embed_jobs(job_rows)
    embed_courses(course_rows)

    print("\n" + "=" * 60)
    print("  Ingest complete.")
    print("=" * 60)
