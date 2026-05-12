import logging
import os

from weaviate.classes.query import MetadataQuery
from weaviate.classes.query import Filter

from db.weaviate_client import get_weaviate
from retrieval.embedder import embed
from retrieval.skills import count_skill_overlap, normalize_skill_name
from retrieval.text_utils import query_terms as extract_query_terms
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

logger = logging.getLogger(__name__)

JOB_CLASS = "Job"
COURSE_CLASS = "Course"
TOP_K_JOBS = int(os.environ.get("RETRIEVAL_TOP_K_JOBS", 5))
TOP_K_COURSES = int(os.environ.get("RETRIEVAL_TOP_K_COURSES", 5))
MIN_JOB_SCORE = float(os.environ.get("RETRIEVAL_MIN_JOB_SCORE", 0.05))
MIN_COURSE_SCORE = float(os.environ.get("RETRIEVAL_MIN_COURSE_SCORE", 0.05))
HYBRID_ALPHA = float(os.environ.get("HYBRID_ALPHA", 0.6))
RRF_K = 60


def _max_pool_by_record(weaviate_objects, id_key: str) -> list[dict]:
    """Group chunk-level Weaviate hits by record ID, keep the max hybrid score per record."""
    by_record: dict[str, dict] = {}
    for obj in weaviate_objects:
        props = obj.properties
        record_id = props.get(id_key)
        if not record_id:
            continue
        score = obj.metadata.score or 0.0
        if record_id not in by_record or score > by_record[record_id]["_raw_score"]:
            by_record[record_id] = {
                id_key: record_id,
                **{k: v for k, v in props.items() if k != id_key},
                "_raw_score": score,
            }
            by_record[record_id][id_key] = record_id
    return list(by_record.values())


def _rrf_rerank(hits: list[dict], rank_keys: list[str], k: int = RRF_K) -> list[dict]:
    """Fuse multiple ranking signals via Reciprocal Rank Fusion."""
    for key in rank_keys:
        sorted_by_key = sorted(hits, key=lambda h: h.get(key, 0.0), reverse=True)
        rank_field = f"_rank_{key}"
        for rank, hit in enumerate(sorted_by_key):
            hit[rank_field] = rank

    for hit in hits:
        rrf_score = sum(
            1.0 / (k + hit.get(f"_rank_{key}", len(hits)))
            for key in rank_keys
        )
        hit["rrf_score"] = round(rrf_score, 6)

    for hit in hits:
        for key in rank_keys:
            hit.pop(f"_rank_{key}", None)

    return sorted(hits, key=lambda h: h["rrf_score"], reverse=True)


@traceable(name="search_jobs", run_type="retriever")
def search_jobs(
    query: str,
    top_k: int = 5,
    job_id_filter: str | None = None,
    student_skills: list[str] | None = None,
    raw_query: str | None = None,
) -> list[dict]:
    """
    Hybrid search (BM25 + semantic) over the Job Weaviate collection with RRF reranking.
    Returns list of { job_id, title, company, skills, score, semantic_score, skill_overlap, rrf_score }.
    """
    client = get_weaviate()
    query_vector = embed(query)
    collection = client.collections.get(JOB_CLASS)

    weaviate_filter = None
    if job_id_filter:
        weaviate_filter = Filter.by_property("job_id").equal(job_id_filter)

    fetch_limit = max(top_k * 5, 20)
    response = collection.query.hybrid(
        query=query,
        vector=query_vector,
        alpha=HYBRID_ALPHA,
        limit=fetch_limit,
        filters=weaviate_filter,
        return_metadata=MetadataQuery(score=True),
    )
    raw_chunks = len(response.objects)

    # Collapse multiple chunk-hits per job down to the best hybrid score.
    pooled = _max_pool_by_record(response.objects, "job_id")
    logger.debug(
        "search_jobs stage=weaviate query=%r fetch_limit=%d raw_chunks=%d pooled_records=%d",
        query[:80], fetch_limit, raw_chunks, len(pooled),
    )

    student_skill_set = {normalize_skill_name(s) for s in (student_skills or []) if s}
    lexical_source = raw_query or query
    terms = extract_query_terms(lexical_source)

    candidates = []
    score_filtered = 0
    for hit in pooled:
        semantic_score = round(hit["_raw_score"], 4)
        if semantic_score < MIN_JOB_SCORE and not job_id_filter:
            score_filtered += 1
            continue
        job_skills = hit.get("skills", []) or []
        overlap = 0
        if student_skill_set and job_skills:
            overlap = len({normalize_skill_name(s) for s in job_skills} & student_skill_set)
        lexical_overlap = count_skill_overlap(list(terms), job_skills)
        title = hit.get("title") or ""
        title_terms = extract_query_terms(title)
        title_overlap = len(terms & title_terms)
        candidates.append({
            "job_id": hit.get("job_id"),
            "title": title,
            "company": hit.get("company"),
            "skills": job_skills,
            "semantic_score": semantic_score,
            "skill_overlap": overlap,
            "query_skill_overlap": lexical_overlap,
            "query_title_overlap": title_overlap,
        })

    logger.debug(
        "search_jobs stage=score_filter min_score=%.3f dropped=%d candidates=%d",
        MIN_JOB_SCORE, score_filtered, len(candidates),
    )

    reranked = _rrf_rerank(candidates, ["semantic_score", "skill_overlap", "query_skill_overlap"])
    for hit in reranked:
        hit["score"] = hit["rrf_score"]

    results = reranked[:top_k]
    logger.debug(
        "search_jobs stage=rrf_rerank top_k=%d returned=%d top_titles=%s",
        top_k, len(results), [h.get("title", "?") for h in results[:3]],
    )
    return results


@traceable(name="search_courses", run_type="retriever")
def search_courses(query: str, top_k: int = 5) -> list[dict]:
    """
    Hybrid search (BM25 + semantic) over the Course Weaviate collection with RRF reranking.
    Returns list of { course_id, course_code, title, skills, score, semantic_score, rrf_score }.
    """
    client = get_weaviate()
    query_vector = embed(query)
    collection = client.collections.get(COURSE_CLASS)

    fetch_limit = max(top_k * 5, 20)
    response = collection.query.hybrid(
        query=query,
        vector=query_vector,
        alpha=HYBRID_ALPHA,
        limit=fetch_limit,
        return_metadata=MetadataQuery(score=True),
    )
    raw_chunks = len(response.objects)

    # Collapse multiple chunk-hits per course down to the best hybrid score.
    pooled = _max_pool_by_record(response.objects, "course_id")
    logger.debug(
        "search_courses stage=weaviate query=%r fetch_limit=%d raw_chunks=%d pooled_records=%d",
        query[:80], fetch_limit, raw_chunks, len(pooled),
    )

    terms = extract_query_terms(query)
    normalized_terms = {normalize_skill_name(t) for t in terms}

    seen_course_codes: set[str] = set()
    candidates = []
    score_filtered = 0
    deduped = 0
    for hit in pooled:
        semantic_score = round(hit["_raw_score"], 4)
        if semantic_score < MIN_COURSE_SCORE:
            score_filtered += 1
            continue
        code = (hit.get("course_code") or "").strip()
        if code and code in seen_course_codes:
            deduped += 1
            continue
        if code:
            seen_course_codes.add(code)
        course_skills = hit.get("skills", []) or []
        title = hit.get("title") or ""
        title_terms = extract_query_terms(title)
        skill_overlap = count_skill_overlap(list(normalized_terms), course_skills)
        title_overlap = len(terms & title_terms)
        candidates.append({
            "course_id": hit.get("course_id"),
            "course_code": code,
            "title": title,
            "skills": course_skills,
            "semantic_score": semantic_score,
            "skill_overlap": skill_overlap,
            "query_skill_overlap": skill_overlap,
            "query_title_overlap": title_overlap,
        })

    logger.debug(
        "search_courses stage=score_filter min_score=%.3f dropped=%d deduped=%d candidates=%d",
        MIN_COURSE_SCORE, score_filtered, deduped, len(candidates),
    )

    reranked = _rrf_rerank(candidates, ["semantic_score", "skill_overlap", "query_skill_overlap"])
    for hit in reranked:
        hit["score"] = hit["rrf_score"]

    results = reranked[:top_k]
    logger.debug(
        "search_courses stage=rrf_rerank top_k=%d returned=%d top_codes=%s",
        top_k, len(results), [h.get("course_code", "?") for h in results[:3]],
    )
    return results
