"""
retrieval/candidates.py

Builds 3 different evidence views from the same bundle.
Same prompt template, different evidence — per the Self-RAG paper.

View A — Specific job:     Top 1 job + courses that close its gaps
View B — Job cluster:      Aggregated summary of all retrieved jobs + broad courses
View C — Course path:      Course-first view focused on learning roadmap
"""

from retrieval.context_builder import bundle_to_context_string


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
        gap_skills = set(top_job.get("gaps", []))
        relevant_courses = [
            c for c in courses
            if any(s in gap_skills for s in c.get("teaches", []))
        ] or courses[:2]

        view_a_bundle = {
            "student": student,
            "jobs": [top_job],
            "courses": relevant_courses,
        }
        views.append({
            "label": "A — Specific Job",
            "context": bundle_to_context_string(view_a_bundle),
            "evidence_description": f"Grounded in: {top_job['title']} @ {top_job['company']}",
        })
    else:
        views.append({
            "label": "A — Specific Job",
            "context": bundle_to_context_string({"student": student, "jobs": [], "courses": courses[:2]}),
            "evidence_description": "No jobs retrieved; course-only context.",
        })

    # ------------------------------------------------------------------
    # View B: Job cluster — aggregate all jobs into a summary
    # ------------------------------------------------------------------
    all_required = []
    all_gaps = []
    all_covered = []
    for j in jobs:
        all_required.extend(j.get("required_skills", []))
        all_gaps.extend(j.get("gaps", []))
        all_covered.extend(j.get("covered", []))

    # Deduplicate and count frequency
    def top_n(items, n=8):
        from collections import Counter
        return [s for s, _ in Counter(items).most_common(n)]

    cluster_job = {
        "job_id": "cluster",
        "title": f"Job Cluster ({len(jobs)} roles)",
        "company": ", ".join(set(j["company"] for j in jobs)),
        "required_skills": top_n(all_required),
        "covered": list(set(all_covered)),
        "gaps": top_n(all_gaps),
        "score": round(sum(j["score"] for j in jobs) / max(len(jobs), 1), 4),
    }

    view_b_bundle = {
        "student": student,
        "jobs": [cluster_job],
        "courses": courses,
    }
    views.append({
        "label": "B — Job Cluster",
        "context": bundle_to_context_string(view_b_bundle),
        "evidence_description": f"Aggregated across {len(jobs)} job postings",
    })

    # ------------------------------------------------------------------
    # View C: Course path — course-first, jobs used only as gap signal
    # ------------------------------------------------------------------
    # Compute overall gap from all jobs combined
    all_gap_skills = set(top_n(all_gaps, 10))
    # Sort courses by how many gaps they cover
    scored_courses = sorted(
        courses,
        key=lambda c: len(set(c.get("teaches", [])) & all_gap_skills),
        reverse=True,
    )

    view_c_bundle = {
        "student": student,
        "jobs": jobs[:2],          # minimal job context for reference
        "courses": scored_courses,  # all courses, sorted by gap coverage
    }
    views.append({
        "label": "C — Course Path",
        "context": bundle_to_context_string(view_c_bundle),
        "evidence_description": f"{len(scored_courses)} courses sorted by gap coverage",
    })

    return views
