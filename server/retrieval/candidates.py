"""
retrieval/candidates.py

Builds 3 different evidence views from the same bundle.
Same prompt template, different evidence — per the Self-RAG paper.

View A — Specific job:     Top 1 job + courses that close its gaps
View B — Job cluster:      Aggregated summary of all retrieved jobs + broad courses
View C — Course path:      Course-first view focused on learning roadmap
"""

from langsmith import traceable

from retrieval.context_builder import bundle_to_context_string
from retrieval.skills import count_skill_overlap, normalize_skill_name, normalized_skill_set


def _annotate_courses_for_gaps(courses: list[dict], gap_skills: set[str]) -> list[dict]:
    annotated: list[dict] = []
    for course in courses:
        teaches = course.get("teaches", []) or []
        covered_gaps = [
            skill for skill in teaches
            if normalize_skill_name(skill) in gap_skills
        ]
        annotated.append({
            **course,
            "addresses_gaps": covered_gaps,
        })
    return annotated


def _courses_with_gap_support(courses: list[dict], gap_skills: set[str]) -> list[dict]:
    annotated = _annotate_courses_for_gaps(courses, gap_skills)
    return [course for course in annotated if course.get("addresses_gaps")]


def _top_courses(courses: list[dict], limit: int = 5) -> list[dict]:
    return sorted(courses, key=lambda course: course.get("score", 0.0), reverse=True)[:limit]


@traceable(name="build_candidate_views", run_type="chain")
def build_candidate_views(bundle: dict) -> list[dict]:
    """
    Returns list of 3 dicts:
      { "label": str, "context": str, "evidence_description": str }
    """
    student = bundle["student"]
    jobs = bundle["jobs"]
    courses = bundle["courses"]

    views = []

    # ------------------------------------------------------------------
    # View A: Specific job — focus on the single highest-scoring job
    # ------------------------------------------------------------------
    if jobs:
        top_job = jobs[0]
        # Only courses that cover gaps for this specific job
        gap_skills = normalized_skill_set(top_job.get("gaps", []))
        relevant_courses = _courses_with_gap_support(courses, gap_skills)
        notes = []
        if gap_skills and not relevant_courses:
            notes.append(
                f"No retrieved courses clearly address these gaps for {top_job['title']}: {', '.join(top_job.get('gaps', []))}."
            )

        view_a_bundle = {
            "student": student,
            "jobs": [top_job],
            "courses": relevant_courses,
            "notes": notes,
        }
        views.append({
            "label": "A — Specific Job",
            "context": bundle_to_context_string(view_a_bundle),
            "evidence_description": f"Grounded in: {top_job['title']} @ {top_job['company']}",
            "bundle": view_a_bundle,
        })
    else:
        fallback_courses = _top_courses(courses, limit=4)
        views.append({
            "label": "A — Specific Job",
            "context": bundle_to_context_string({"student": student, "jobs": [], "courses": fallback_courses}),
            "evidence_description": "No jobs retrieved; course-only context.",
            "bundle": {"student": student, "jobs": [], "courses": fallback_courses},
        })

    # ------------------------------------------------------------------
    # View B: Job cluster — keep top jobs explicit to avoid hallucinated titles
    # ------------------------------------------------------------------
    cluster_gap_skills = normalized_skill_set([gap for job in jobs for gap in job.get("gaps", [])])
    cluster_courses = _courses_with_gap_support(courses, cluster_gap_skills)
    if not cluster_courses:
        cluster_courses = _top_courses(courses, limit=5)
    view_b_bundle = {
        "student": student,
        "jobs": jobs[:7],
        "courses": cluster_courses,
    }
    views.append({
        "label": "B — Job Cluster",
        "context": bundle_to_context_string(view_b_bundle),
        "evidence_description": f"Aggregated across {len(jobs)} job postings",
        "bundle": view_b_bundle,
    })

    # ------------------------------------------------------------------
    # View C: Course path — course-first, jobs used only as gap signal
    # ------------------------------------------------------------------
    # Compute overall gap from all jobs combined
    all_gaps = []
    for j in jobs:
        all_gaps.extend(j.get("gaps", []))
    from collections import Counter
    normalized_gaps = [normalize_skill_name(gap) for gap in all_gaps if normalize_skill_name(gap)]
    all_gap_skills = {
        skill
        for skill, _ in Counter(normalized_gaps).most_common(10)
    }
    # Sort courses by how many gaps they cover
    scored_courses = sorted(
        courses,
        key=lambda c: count_skill_overlap(c.get("teaches", []), list(all_gap_skills)),
        reverse=True,
    )
    if all_gap_skills:
        supported_courses = _courses_with_gap_support(scored_courses, all_gap_skills)
        scored_courses = supported_courses or _top_courses(scored_courses, limit=6)
    else:
        scored_courses = _top_courses(scored_courses, limit=6)

    view_c_bundle = {
        "student": student,
        "jobs": jobs[:2],          # minimal job context for reference
        "courses": scored_courses,
        "notes": (
            [f"No retrieved courses clearly address the top combined gaps: {', '.join(sorted(all_gap_skills))}."]
            if all_gap_skills and not _courses_with_gap_support(courses, all_gap_skills)
            else []
        ),
    }
    views.append({
        "label": "C — Course Path",
        "context": bundle_to_context_string(view_c_bundle),
        "evidence_description": f"{len(scored_courses)} courses sorted by gap coverage",
        "bundle": view_c_bundle,
    })

    return views
