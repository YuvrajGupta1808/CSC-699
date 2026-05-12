"""
Rebuild the Weaviate Course collection from current Supabase course rows.

One Weaviate object is created per text chunk (not per course), enabling
max-similarity pooling at query time. The course_id field is stored in the
payload so the search layer can group chunks back to their source record.

Run:
  PYTHONPATH=server python weaviate/index_courses.py
"""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

from weaviate.classes.config import Configure, Property, DataType

from db.supabase_client import get_supabase
from db.weaviate_client import get_weaviate
from retrieval.embedder import embed
from retrieval.job_content import chunk_text
from retrieval.record_utils import course_skills_value
from retrieval.skills import extract_skill_names

COURSE_CLASS = "Course"


def _skills_field() -> str:
    sb = get_supabase()
    try:
        sb.table("courses").select("skills_courses").limit(1).execute()
        return "skills_courses"
    except Exception:
        return "skills_courses_json"


def load_courses() -> list[dict]:
    sb = get_supabase()
    skills_field = _skills_field()
    rows = (
        sb.table("courses")
        .select(f"course_id,course_code,title,description,{skills_field}")
        .execute()
        .data
    )
    return rows or []


def recreate_collection() -> None:
    client = get_weaviate()
    if client.collections.exists(COURSE_CLASS):
        client.collections.delete(COURSE_CLASS)

    client.collections.create(
        name=COURSE_CLASS,
        vector_config=Configure.Vectors.self_provided(),
        properties=[
            # Filterable identifier — excluded from BM25
            Property(name="course_id", data_type=DataType.TEXT,
                     skip_vectorization=True, index_filterable=True, index_searchable=False),
            # BM25-searchable text fields
            Property(name="course_code", data_type=DataType.TEXT,
                     skip_vectorization=True, index_filterable=False, index_searchable=True),
            Property(name="title", data_type=DataType.TEXT,
                     skip_vectorization=True, index_filterable=False, index_searchable=True),
            Property(name="chunk_text", data_type=DataType.TEXT,
                     skip_vectorization=True, index_filterable=False, index_searchable=True),
            # Skills array — BM25-searchable for exact skill name matching
            Property(name="skills", data_type=DataType.TEXT_ARRAY,
                     skip_vectorization=True, index_filterable=False, index_searchable=True),
            # Chunk metadata — not searchable
            Property(name="chunk_index", data_type=DataType.INT,
                     skip_vectorization=True, index_filterable=False, index_searchable=False),
            Property(name="total_chunks", data_type=DataType.INT,
                     skip_vectorization=True, index_filterable=False, index_searchable=False),
        ],
    )


def index_courses(course_rows: list[dict]) -> int:
    """Insert course chunk-objects into Weaviate. Returns total chunk count."""
    client = get_weaviate()
    collection = client.collections.get(COURSE_CLASS)
    total_chunks = 0

    with collection.batch.dynamic() as batch:
        for course in course_rows:
            skills = extract_skill_names(course_skills_value(course))
            skills_text = " ".join(skills)
            text = (
                f"{course.get('course_code', '')} {course.get('title', '')} "
                f"{course.get('description', '')} {skills_text}"
            ).strip()
            chunks = chunk_text(text, max_chars=1400, overlap=200) or [text or ""]
            n_chunks = len(chunks)
            for idx, chunk in enumerate(chunks):
                vector = embed(chunk)
                batch.add_object(
                    properties={
                        "course_id": course["course_id"],
                        "course_code": course.get("course_code") or "",
                        "title": course.get("title") or "",
                        "skills": skills,
                        "chunk_text": chunk,
                        "chunk_index": idx,
                        "total_chunks": n_chunks,
                    },
                    vector=vector,
                )
                total_chunks += 1

    return total_chunks


def main() -> None:
    course_rows = load_courses()
    if not course_rows:
        raise SystemExit("No course rows found in Supabase.")

    recreate_collection()
    chunk_count = index_courses(course_rows)
    course_count = len(course_rows)
    avg = chunk_count / course_count if course_count else 0
    print(f"Indexed {course_count} courses → {chunk_count} chunk objects ({avg:.1f} avg/course) into Weaviate '{COURSE_CLASS}'.")
    print("Sample:", ", ".join(c.get("course_code", "") for c in course_rows[:5]))


if __name__ == "__main__":
    main()
