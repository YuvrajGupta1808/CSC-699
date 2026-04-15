"""
Sync only the course catalog into Supabase while preserving existing course IDs.

Run:
  python server/sync_courses_to_supabase.py
"""

from __future__ import annotations

import csv
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

from db.supabase_client import get_supabase


COURSES_CSV = REPO_ROOT / "data" / "sfsu_csc_courses_clean_skills.csv"
VERIFICATION_CODES = ["CSC 317", "CSC 648", "CSC 849", "CSC 867", "CSC 872"]


def parse_course_skills(raw: str) -> list[dict]:
    pattern = re.findall(r"\(([^,)]+),\s*(\d+)\)", raw)
    return [{"skill": skill.strip(), "weight": int(weight)} for skill, weight in pattern]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def verify_courses_table() -> None:
    sb = get_supabase()
    sb.table("courses").select("course_id").limit(1).execute()


def print_verification_rows() -> None:
    sb = get_supabase()
    for code in VERIFICATION_CODES:
        data = (
            sb.table("courses")
            .select("course_code,title,skills_courses_json")
            .eq("course_code", code)
            .limit(1)
            .execute()
            .data
        )
        if not data:
            print(f"VERIFY {code}: missing")
            continue
        row = data[0]
        skills = ", ".join(item["skill"] for item in (row.get("skills_courses_json") or [])[:5])
        print(f"VERIFY {row['course_code']}: {skills}")


def main() -> None:
    verify_courses_table()
    sb = get_supabase()

    existing_rows = sb.table("courses").select("course_id,course_code").execute().data
    existing_ids = {
        (row.get("course_code") or "").strip(): row.get("course_id")
        for row in existing_rows
        if row.get("course_code") and row.get("course_id")
    }

    rows = []
    with COURSES_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            course_code = (row.get("course_code") or "").strip()
            rows.append({
                "course_id": existing_ids.get(course_code) or str(uuid.uuid4()),
                "course_code": course_code,
                "title": (row.get("title") or "").strip(),
                "description": (row.get("description") or "").strip(),
                "skills_courses_json": parse_course_skills(row.get("skills", "")),
                "updated_at": now_iso(),
            })

    sb.table("courses").upsert(rows, on_conflict="course_code").execute()
    print(f"Synced {len(rows)} course rows to Supabase.")
    print_verification_rows()


if __name__ == "__main__":
    main()
