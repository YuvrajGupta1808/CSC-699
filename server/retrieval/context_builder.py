from db.supabase_client import get_supabase
from langsmith import traceable


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
    student_skills: list[str] = _extract_skill_names(student.get("skill_profile_json") or [])
    completed_courses: list[str] = student.get("completed_courses_json") or []

    # --- Jobs: enrich from Supabase ---
    enriched_jobs = []
    for hit in job_hits:
        job_row = None
        job_id = hit.get("job_id")
        if job_id:
            rows = (
                sb.table("jobs")
                .select("job_id, title, company, skills_jobs_json, description")
                .eq("job_id", job_id)
                .limit(1)
                .execute()
                .data
                or []
            )
            if rows:
                job_row = rows[0]

        # Fallback: if job_id is stale/missing, try matching by title+company.
        if not job_row and hit.get("title") and hit.get("company"):
            rows = (
                sb.table("jobs")
                .select("job_id, title, company, skills_jobs_json, description")
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
            # Skip stale vector hit instead of crashing the whole response.
            continue

        job_skills = _extract_skill_names(job_row.get("skills_jobs_json") or [])
        covered = [s for s in job_skills if s in student_skills]
        gaps = [s for s in job_skills if s not in student_skills]
        enriched_jobs.append({
            **hit,
            "job_id": job_row.get("job_id", hit.get("job_id")),
            "title": job_row.get("title", hit.get("title")),
            "company": job_row.get("company", hit.get("company")),
            "required_skills": job_skills,
            "covered": covered,
            "gaps": gaps,
        })

    # --- Courses: enrich from Supabase ---
    enriched_courses = []
    seen_courses: set[str] = set()
    for hit in course_hits:
        course_row = None
        course_id = hit.get("course_id")
        course_code = (hit.get("course_code") or "").strip()

        if course_id:
            rows = (
                sb.table("courses")
                .select("course_id, course_code, title, skills_courses_json")
                .eq("course_id", course_id)
                .limit(1)
                .execute()
                .data
                or []
            )
            if rows:
                course_row = rows[0]

        # Fallback lookup for stale course_id values from old vector payloads.
        if not course_row and course_code:
            rows = (
                sb.table("courses")
                .select("course_id, course_code, title, skills_courses_json")
                .eq("course_code", course_code)
                .limit(1)
                .execute()
                .data
                or []
            )
            if rows:
                course_row = rows[0]

        if not course_row:
            # Skip stale vector hit instead of crashing the whole response.
            continue

        dedup_key = course_row.get("course_id") or course_row.get("course_code") or course_code
        if dedup_key in seen_courses:
            continue
        seen_courses.add(dedup_key)

        course_skills = _extract_skill_names(course_row.get("skills_courses_json") or [])
        enriched_courses.append({
            **hit,
            "course_id": course_row.get("course_id", hit.get("course_id")),
            "course_code": course_row.get("course_code", hit.get("course_code")),
            "title": course_row.get("title", hit.get("title")),
            "teaches": course_skills,
        })

    return {
        "student": {
            "name": student["name"],
            "major": student["major"],
            "skills": student_skills,
            "completed_courses": completed_courses,
        },
        "jobs": enriched_jobs,
        "courses": enriched_courses,
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
        lines.append("RELEVANT JOB POSTINGS")
        for j in bundle["jobs"]:
            lines.append(f"- {j['title']} at {j['company']} (relevance: {j['score']})")
            lines.append(f"  Required: {', '.join(j['required_skills'])}")
            lines.append(f"  Student covers: {', '.join(j['covered']) or 'none'}")
            lines.append(f"  Gaps: {', '.join(j['gaps']) or 'none'}")
        lines.append("")

    if bundle["courses"]:
        lines.append("RELEVANT COURSES")
        for c in bundle["courses"]:
            lines.append(f"- {c['course_code']}: {c['title']} (relevance: {c['score']})")
            lines.append(f"  Teaches: {', '.join(c['teaches'])}")
        lines.append("")

    return "\n".join(lines)


def _extract_skill_names(skills_json) -> list[str]:
    """
    Normalize skills field — handles both:
      [{"skill": "Python", "weight": 40}, ...]   (jobs format)
      [["Python", 40], ...]                       (courses format)
      ["Python", ...]                             (plain list)
    """
    if not skills_json:
        return []
    names = []
    for item in skills_json:
        if isinstance(item, dict):
            names.append(item.get("skill") or item.get("name") or "")
        elif isinstance(item, (list, tuple)) and len(item) >= 1:
            names.append(str(item[0]))
        elif isinstance(item, str):
            names.append(item)
    return [n.strip() for n in names if n.strip()]
