import os
from qdrant_client.models import Filter, FieldCondition, MatchValue
from db.qdrant_client import get_qdrant
from retrieval.embedder import embed
from dotenv import load_dotenv

load_dotenv()

JOBS_COLLECTION = "jobs_collection"
COURSES_COLLECTION = "courses_collection"
TOP_K_JOBS = int(os.environ.get("RETRIEVAL_TOP_K_JOBS", 5))
TOP_K_COURSES = int(os.environ.get("RETRIEVAL_TOP_K_COURSES", 5))


def search_jobs(
    query: str,
    top_k: int = 5,
    job_id_filter: str | None = None,
    student_skills: list[str] | None = None,
) -> list[dict]:
    """
    Semantic search over jobs_collection.
    Optionally filter to a specific job_id.
    Returns list of { job_id, title, company, skills, score }.
    """
    client = get_qdrant()
    query_vector = embed(query)

    qdrant_filter = None
    if job_id_filter:
        qdrant_filter = Filter(
            must=[FieldCondition(key="job_id", match=MatchValue(value=job_id_filter))]
        )

    results = client.query_points(
        collection_name=JOBS_COLLECTION,
        query=query_vector,
        limit=max(top_k * 3, top_k),
        query_filter=qdrant_filter,
        with_payload=True,
    )

    hits = []
    student_skill_set = {s.strip().lower() for s in (student_skills or []) if s}
    for r in results.points:
        job_skills = r.payload.get("skills", []) or []
        overlap = 0
        if student_skill_set and job_skills:
            overlap = len({s.lower() for s in job_skills} & student_skill_set)
        # Blend semantic score with student-skill overlap for personalization.
        personalized_score = round((r.score or 0.0) + overlap * 0.02, 4)
        hits.append({
            "job_id": r.payload.get("job_id"),
            "title": r.payload.get("title"),
            "company": r.payload.get("company"),
            "skills": job_skills,
            "score": personalized_score,
            "semantic_score": round(r.score, 4),
            "skill_overlap": overlap,
        })
    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits[:top_k]


def search_courses(query: str, top_k: int = 5) -> list[dict]:
    """
    Semantic search over courses_collection.
    Returns list of { course_id, course_code, title, skills, score }.
    """
    client = get_qdrant()
    query_vector = embed(query)

    results = client.query_points(
        collection_name=COURSES_COLLECTION,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    hits = []
    for r in results.points:
        hits.append({
            "course_id": r.payload.get("course_id"),
            "course_code": r.payload.get("course_code"),
            "title": r.payload.get("title"),
            "skills": r.payload.get("skills", []),
            "score": round(r.score, 4),
        })
    return hits
