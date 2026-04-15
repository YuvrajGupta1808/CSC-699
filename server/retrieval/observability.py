from __future__ import annotations

import os
from typing import Any

from langsmith import uuid7
from langsmith.run_helpers import get_current_run_tree


def langsmith_enabled() -> bool:
    return os.environ.get("LANGSMITH_TRACING", "").strip().lower() == "true"


def langsmith_project() -> str | None:
    return os.environ.get("LANGSMITH_PROJECT") or None


def new_trace_id() -> str:
    return str(uuid7())


def short_text(value: str | None, limit: int = 240) -> str:
    if not value:
        return ""
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def attach_run_metadata(metadata: dict[str, Any] | None = None, tags: list[str] | None = None) -> None:
    run = get_current_run_tree()
    if run is None:
        return
    if metadata:
        run.add_metadata(metadata)
    if tags:
        run.add_tags(tags)
    run.patch()


def summarize_student_profile(profile: dict[str, Any]) -> dict[str, Any]:
    skills = [
        item.get("skill")
        for item in (profile.get("skill_profile_json") or [])
        if isinstance(item, dict) and item.get("skill")
    ]
    return {
        "student_id": profile.get("student_id"),
        "name": profile.get("name"),
        "major": profile.get("major"),
        "completed_courses": profile.get("completed_courses_json") or [],
        "skill_count": len(skills),
        "skills": skills[:12],
    }


def summarize_job_hits(job_hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "job_id": hit.get("job_id"),
            "title": hit.get("title"),
            "company": hit.get("company"),
            "score": hit.get("score"),
            "semantic_score": hit.get("semantic_score"),
            "skill_overlap": hit.get("skill_overlap"),
            "skills": (hit.get("skills") or [])[:10],
        }
        for hit in job_hits
    ]


def summarize_course_hits(course_hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "course_id": hit.get("course_id"),
            "course_code": hit.get("course_code"),
            "title": hit.get("title"),
            "score": hit.get("score"),
            "skills": (hit.get("skills") or [])[:10],
        }
        for hit in course_hits
    ]


def summarize_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "student": bundle.get("student", {}),
        "jobs": [
            {
                "job_id": job.get("job_id"),
                "title": job.get("title"),
                "company": job.get("company"),
                "score": job.get("score"),
                "required_skills": (job.get("required_skills") or [])[:12],
                "covered": job.get("covered") or [],
                "gaps": job.get("gaps") or [],
            }
            for job in bundle.get("jobs", [])
        ],
        "courses": [
            {
                "course_id": course.get("course_id"),
                "course_code": course.get("course_code"),
                "title": course.get("title"),
                "score": course.get("score"),
                "teaches": (course.get("teaches") or [])[:12],
            }
            for course in bundle.get("courses", [])
        ],
    }


def summarize_candidate_views(views: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "label": view.get("label"),
            "evidence_description": view.get("evidence_description"),
            "context_chars": len(view.get("context", "")),
            "context_preview": short_text(view.get("context", ""), limit=400),
        }
        for view in views
    ]


def summarize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    view = candidate.get("view", {})
    scores = candidate.get("scores") or {}
    return {
        "label": view.get("label"),
        "evidence_description": view.get("evidence_description"),
        "response_chars": len(candidate.get("text", "")),
        "response_preview": short_text(candidate.get("text", ""), limit=400),
        "scores": scores,
    }


def summarize_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [summarize_candidate(candidate) for candidate in candidates]


def summarize_ranked_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = sorted(
        candidates,
        key=lambda candidate: (candidate.get("scores") or {}).get("total", 0.0),
        reverse=True,
    )
    return [
        {
            "label": candidate.get("view", {}).get("label"),
            "total": (candidate.get("scores") or {}).get("total"),
            "relevance": (candidate.get("scores") or {}).get("relevance"),
            "support": (candidate.get("scores") or {}).get("support"),
            "utility": (candidate.get("scores") or {}).get("utility"),
            "critique": (candidate.get("scores") or {}).get("critique"),
        }
        for candidate in ranked
    ]
