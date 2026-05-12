"""
Rebuild the Weaviate Job collection from current Supabase job rows.

One Weaviate object is created per text chunk (not per job), enabling
max-similarity pooling at query time. The job_id field is stored in the
payload so the search layer can group chunks back to their source record.

Run:
  PYTHONPATH=server python weaviate/index_jobs.py
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
from retrieval.job_content import build_job_embedding_text, chunk_text
from retrieval.record_utils import job_skills_value

JOB_CLASS = "Job"


def _skills_field() -> str:
    sb = get_supabase()
    try:
        sb.table("jobs").select("skills_jobs").limit(1).execute()
        return "skills_jobs"
    except Exception:
        return "skills_jobs_json"


def load_jobs() -> list[dict]:
    sb = get_supabase()
    skills_field = _skills_field()
    rows = (
        sb.table("jobs")
        .select(f"job_id,title,company,location,description,{skills_field}")
        .execute()
        .data
    )
    return rows or []


def recreate_collection() -> None:
    client = get_weaviate()
    if client.collections.exists(JOB_CLASS):
        client.collections.delete(JOB_CLASS)

    client.collections.create(
        name=JOB_CLASS,
        vector_config=Configure.Vectors.self_provided(),
        properties=[
            # Filterable identifier — excluded from BM25
            Property(name="job_id", data_type=DataType.TEXT,
                     skip_vectorization=True, index_filterable=True, index_searchable=False),
            # BM25-searchable text fields
            Property(name="title", data_type=DataType.TEXT,
                     skip_vectorization=True, index_filterable=False, index_searchable=True),
            Property(name="company", data_type=DataType.TEXT,
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


def index_jobs(job_rows: list[dict]) -> int:
    """Insert job chunk-objects into Weaviate. Returns total chunk count."""
    client = get_weaviate()
    collection = client.collections.get(JOB_CLASS)
    total_chunks = 0

    with collection.batch.dynamic() as batch:
        for job in job_rows:
            skills = job_skills_value(job)
            text = build_job_embedding_text(job)
            chunks = chunk_text(text, max_chars=1400, overlap=200) or [text or ""]
            n_chunks = len(chunks)
            for idx, chunk in enumerate(chunks):
                vector = embed(chunk)
                batch.add_object(
                    properties={
                        "job_id": job["job_id"],
                        "title": job.get("title") or "",
                        "company": job.get("company") or "",
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
    job_rows = load_jobs()
    if not job_rows:
        raise SystemExit("No job rows found in Supabase.")

    recreate_collection()
    chunk_count = index_jobs(job_rows)
    job_count = len(job_rows)
    avg = chunk_count / job_count if job_count else 0
    print(f"Indexed {job_count} jobs → {chunk_count} chunk objects ({avg:.1f} avg/job) into Weaviate '{JOB_CLASS}'.")
    print("Sample:", ", ".join(j.get("title", "") for j in job_rows[:5]))


if __name__ == "__main__":
    main()
