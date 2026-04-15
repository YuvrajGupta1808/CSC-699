"""
Rebuild the Qdrant course vector collection from current Supabase course rows.

This is intended for the case where course skill metadata changes and the old
Qdrant payloads/vectors need to be fully replaced rather than incrementally
upserted.

Run:
  server/.venv/bin/python server/rebuild_course_vectors.py
"""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from qdrant_client.models import Distance, PointStruct, VectorParams


REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

from db.qdrant_client import get_qdrant
from db.supabase_client import get_supabase
from retrieval.embedder import embed


COURSES_COLLECTION = "courses_collection"
VECTOR_SIZE = 768


def load_courses() -> list[dict]:
    sb = get_supabase()
    rows = sb.table("courses").select(
        "course_id,course_code,title,description,skills_courses_json"
    ).execute().data
    return rows or []


def recreate_collection() -> None:
    client = get_qdrant()
    existing = {collection.name for collection in client.get_collections().collections}
    if COURSES_COLLECTION in existing:
        client.delete_collection(COURSES_COLLECTION)
    client.create_collection(
        collection_name=COURSES_COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )


def build_points(course_rows: list[dict]) -> list[PointStruct]:
    points: list[PointStruct] = []
    for course in course_rows:
        skills = course.get("skills_courses_json") or []
        skills_text = " ".join(item["skill"] for item in skills if item.get("skill"))
        text = (
            f"{course['course_code']} {course['title']} "
            f"{course.get('description', '')} {skills_text}"
        )
        vector = embed(text)
        points.append(
            PointStruct(
                id=course["course_id"],
                vector=vector,
                payload={
                    "course_id": course["course_id"],
                    "course_code": course["course_code"],
                    "title": course["title"],
                    "skills": [item["skill"] for item in skills if item.get("skill")],
                },
            )
        )
    return points


def upsert_points(points: list[PointStruct]) -> None:
    client = get_qdrant()
    batch_size = 25
    for index in range(0, len(points), batch_size):
        client.upsert(
            collection_name=COURSES_COLLECTION,
            points=points[index:index + batch_size],
        )


def main() -> None:
    course_rows = load_courses()
    if not course_rows:
        raise SystemExit("No course rows found in Supabase.")

    recreate_collection()
    points = build_points(course_rows)
    upsert_points(points)

    print(f"Rebuilt {COURSES_COLLECTION} with {len(points)} course vectors.")
    sample_codes = [course["course_code"] for course in course_rows[:5]]
    print("Sample course codes:", ", ".join(sample_codes))


if __name__ == "__main__":
    main()
