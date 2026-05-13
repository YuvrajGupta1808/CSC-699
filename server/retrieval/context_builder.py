from db.supabase_client import get_supabase
from langsmith import traceable

from retrieval.record_utils import (
    course_skills_value,
    job_skills_value,
    student_completed_courses_value,
    student_skill_profile_value,
)
from retrieval.skills import compute_skill_overlap, extract_skill_names


def _trim_evidence_text(value: str, limit: int = 500) -> str:
    compact = " ".join((value or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def get_student_profile(student_id: str) -> dict:
    """Fetch full student row from Supabase."""
    sb = get_supabase()
    result = sb.table("students").select("*").eq("student_id", student_id).single().execute()
    return result.data


def get_all_students() -> list[dict]:
    """Fetch all students for the UI dropdown."""
    sb = get_supabase()
    result = sb.table("students").select("student_id, name, major").execute()
    return result.data


def get_all_jobs() -> list[dict]:
    """Fetch job titles for the optional job filter dropdown."""
    sb = get_supabase()
    result = sb.table("jobs").select("job_id, title, company").execute()
    return result.data


def _fetch_rows_by_ids(sb, table: str, key: str, ids: list[str]) -> dict[str, dict]:
    clean_ids = [value for value in ids if value]
    if not clean_ids:
        return {}
    rows = sb.table(table).select("*").in_(key, clean_ids).execute().data or []
    return {row[key]: row for row in rows if row.get(key)}


def _fetch_rows_by_codes(sb, table: str, key: str, codes: list[str]) -> dict[str, dict]:
    clean_codes = [value for value in codes if value]
    if not clean_codes:
        return {}
    rows = sb.table(table).select("*").in_(key, clean_codes).execute().data or []
    return {row[key]: row for row in rows if row.get(key)}


@traceable(name="build_evidence_bundle", run_type="chain")
def build_evidence_bundle(
    student_id: str,
    job_hits: list[dict],
    course_hits: list[dict],
) -> dict:
    """
    Enrich retrieved hits with full Supabase data and compute skill gaps.
    Returns a structured evidence bundle ready for the prompt.
    """
    sb = get_supabase()

    # --- Student ---
    student = get_student_profile(student_id)
    student_skills: list[str] = extract_skill_names(student_skill_profile_value(student))
    completed_courses: list[str] = student_completed_courses_value(student)

    # --- Jobs: enrich from Supabase ---
    job_rows_by_id = _fetch_rows_by_ids(
        sb,
        "jobs",
        "job_id",
        [hit.get("job_id") for hit in job_hits],
    )
    warnings: list[str] = []
    enriched_jobs = []
    for hit in job_hits:
        job_row = job_rows_by_id.get(hit.get("job_id"))

        # Fallback: if job_id is stale/missing, try matching by title+company.
        if not job_row and hit.get("title") and hit.get("company"):
            rows = (
                sb.table("jobs")
                .select("*")
                .eq("title", hit["title"])
                .eq("company", hit["company"])
                .limit(1)
                .execute()
                .data
                or []
            )
            if rows:
                job_row = rows[0]

        if not job_row:
            warnings.append(f"[WARN] job_id {hit.get('job_id')!r} not found in Supabase after vector hit")
            continue

        job_skills = extract_skill_names(job_skills_value(job_row))
        covered, gaps = compute_skill_overlap(job_skills, student_skills)
        enriched_jobs.append({
            **hit,
            "job_id": job_row.get("job_id", hit.get("job_id")),
            "title": job_row.get("title", hit.get("title")),
            "company": job_row.get("company", hit.get("company")),
            "required_skills": job_skills,
            "covered": covered,
            "gaps": gaps,
            "description_excerpt": _trim_evidence_text(job_row.get("description", "")),
        })

    # --- Courses: enrich from Supabase ---
    course_rows_by_id = _fetch_rows_by_ids(
        sb,
        "courses",
        "course_id",
        [hit.get("course_id") for hit in course_hits],
    )
    course_rows_by_code = _fetch_rows_by_codes(
        sb,
        "courses",
        "course_code",
        [(hit.get("course_code") or "").strip() for hit in course_hits],
    )
    enriched_courses = []
    seen_courses: set[str] = set()
    for hit in course_hits:
        course_id = hit.get("course_id")
        course_code = (hit.get("course_code") or "").strip()
        course_row = course_rows_by_id.get(course_id)

        # Fallback lookup for stale course_id values from old vector payloads.
        if not course_row and course_code:
            course_row = course_rows_by_code.get(course_code)

        if not course_row:
            warnings.append(
                f"[WARN] course_id {hit.get('course_id')!r} / course_code {hit.get('course_code')!r} not found in Supabase after vector hit"
            )
            continue

        dedup_key = course_row.get("course_id") or course_row.get("course_code") or course_code
        if dedup_key in seen_courses:
            continue
        seen_courses.add(dedup_key)

        course_skills = extract_skill_names(course_skills_value(course_row))
        enriched_courses.append({
            **hit,
            "course_id": course_row.get("course_id", hit.get("course_id")),
            "course_code": course_row.get("course_code", hit.get("course_code")),
            "title": course_row.get("title", hit.get("title")),
            "teaches": course_skills,
            "description_excerpt": _trim_evidence_text(course_row.get("description", "")),
        })

    stale_job_count = len(job_hits) - len(enriched_jobs)
    stale_course_count = len(course_hits) - len(enriched_courses)
    if stale_job_count > 0 or stale_course_count > 0:
        warnings.append(
            f"[HEALTH] {stale_job_count} stale job hit(s), {stale_course_count} stale course hit(s) dropped during enrichment"
        )

    return {
        "student": {
            "name": student["name"],
            "major": student["major"],
            "skills": student_skills,
            "completed_courses": completed_courses,
        },
        "jobs": enriched_jobs,
        "courses": enriched_courses,
        "retrieval_warnings": warnings,
    }


@traceable(name="bundle_to_context_string", run_type="chain")
def bundle_to_context_string(bundle: dict) -> str:
    """
    Convert an evidence bundle into a plain-text context string for the LLM prompt.
    """
    s = bundle["student"]
    lines = [
        f"STUDENT PROFILE",
        f"Name: {s['name']}",
        f"Major: {s['major']}",
        f"Current skills: {', '.join(s['skills']) or 'none listed'}",
        f"Completed courses: {', '.join(s['completed_courses']) or 'none listed'}",
        "",
    ]

    if bundle["jobs"]:
        lines.append(f"RELEVANT JOB POSTINGS (top {len(bundle['jobs'])} retrieved — not an exhaustive list)")
        for j in bundle["jobs"]:
            lines.append(f"- {j['title']} at {j['company']}")
            lines.append(f"  Required: {', '.join(j['required_skills'])}")
            lines.append(f"  Student covers: {', '.join(j['covered']) or 'none'}")
            lines.append(f"  Gaps: {', '.join(j['gaps']) or 'none'}")
            if j.get("description_excerpt"):
                lines.append(f"  Source excerpt (job description): {j['description_excerpt']}")
        lines.append("")

    if bundle.get("notes"):
        lines.append("RETRIEVAL NOTES")
        for note in bundle["notes"]:
            lines.append(f"- {note}")
        lines.append("")

    if bundle["courses"]:
        lines.append(f"RELEVANT COURSES (top {len(bundle['courses'])} retrieved — not an exhaustive list)")
        for c in bundle["courses"]:
            lines.append(f"- {c['course_code']}: {c['title']}")
            lines.append(f"  Teaches: {', '.join(c['teaches'])}")
            if c.get("addresses_gaps"):
                lines.append(f"  Addresses gaps: {', '.join(c['addresses_gaps'])}")
            if c.get("description_excerpt"):
                lines.append(f"  Source excerpt (course description): {c['description_excerpt']}")
        lines.append("")

    return "\n".join(lines)
