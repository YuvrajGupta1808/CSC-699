from __future__ import annotations

import os
import time
from functools import lru_cache
from typing import Any

from langsmith import Client, uuid7
from langsmith.run_trees import RunTree
from langsmith.run_helpers import get_current_run_tree

from retrieval.record_utils import student_completed_courses_value, student_skill_profile_value


def langsmith_enabled() -> bool:
    return os.environ.get("LANGSMITH_TRACING", "").strip().lower() == "true"


def langsmith_project() -> str | None:
    return os.environ.get("LANGSMITH_PROJECT") or None


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def langsmith_feedback_enabled() -> bool:
    return langsmith_enabled() and _env_flag("LANGSMITH_AUTO_FEEDBACK", default=True)


def langsmith_reference_examples_enabled() -> bool:
    return langsmith_enabled() and _env_flag("LANGSMITH_AUTO_REFERENCE_EXAMPLES", default=True)


def langsmith_dataset_name() -> str:
    configured = os.environ.get("LANGSMITH_DATASET")
    if configured:
        return configured
    project = langsmith_project() or "advisor"
    return f"{project}-reference-examples"


def ollama_input_token_cost() -> float:
    return float(os.environ.get("OLLAMA_INPUT_TOKEN_COST_USD", "0"))


def ollama_output_token_cost() -> float:
    return float(os.environ.get("OLLAMA_OUTPUT_TOKEN_COST_USD", "0"))


@lru_cache(maxsize=1)
def langsmith_client() -> Client | None:
    if not langsmith_enabled():
        return None
    try:
        return Client()
    except Exception:
        return None


@lru_cache(maxsize=8)
def ensure_dataset(dataset_name: str):
    client = langsmith_client()
    if client is None:
        return None
    try:
        return client.read_dataset(dataset_name=dataset_name)
    except Exception:
        try:
            return client.create_dataset(
                dataset_name=dataset_name,
                description="Auto-generated advisor reference examples from LangGraph traces.",
                metadata={"source": "advisor", "automation": "reference_examples"},
            )
        except Exception:
            return None


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


def summarize_retrieval_warnings(warnings: list[str]) -> dict[str, Any]:
    return {"count": len(warnings), "sample": warnings[:3]}


def summarize_student_profile(profile: dict[str, Any]) -> dict[str, Any]:
    skills = [
        item for item in student_skill_profile_value(profile) if isinstance(item, str)
    ]
    return {
        "student_id": profile.get("student_id"),
        "name": profile.get("name"),
        "major": profile.get("major"),
        "completed_courses": student_completed_courses_value(profile),
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


def ollama_usage_metadata(response_payload: dict[str, Any]) -> dict[str, Any]:
    input_tokens = int(response_payload.get("prompt_eval_count") or 0)
    output_tokens = int(response_payload.get("eval_count") or 0)
    total_tokens = input_tokens + output_tokens
    input_cost = input_tokens * ollama_input_token_cost()
    output_cost = output_tokens * ollama_output_token_cost()
    usage: dict[str, Any] = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
    }
    if response_payload.get("prompt_eval_count") is not None:
        usage["input_token_details"] = {"prompt_tokens": input_tokens}
    if response_payload.get("eval_count") is not None:
        usage["output_token_details"] = {"completion_tokens": output_tokens}
    return usage


def ollama_timing_metadata(response_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "load_seconds": round((response_payload.get("load_duration") or 0) / 1_000_000_000, 6),
        "prompt_eval_seconds": round((response_payload.get("prompt_eval_duration") or 0) / 1_000_000_000, 6),
        "completion_seconds": round((response_payload.get("eval_duration") or 0) / 1_000_000_000, 6),
        "total_seconds": round((response_payload.get("total_duration") or 0) / 1_000_000_000, 6),
    }


def enrich_llm_run(
    run: RunTree,
    *,
    outputs: dict[str, Any],
    metadata: dict[str, Any],
    usage_metadata: dict[str, Any],
    first_token_time,
) -> None:
    run.set(outputs=outputs, metadata=metadata, usage_metadata=usage_metadata)
    run.end(metadata=metadata)
    run.patch()

    client = langsmith_client()
    if client is None:
        return

    update_payload: dict[str, Any] = {
        "first_token_time": first_token_time,
        "prompt_tokens": usage_metadata.get("input_tokens"),
        "completion_tokens": usage_metadata.get("output_tokens"),
        "total_tokens": usage_metadata.get("total_tokens"),
        "prompt_cost": usage_metadata.get("input_cost"),
        "completion_cost": usage_metadata.get("output_cost"),
        "total_cost": usage_metadata.get("total_cost"),
    }
    try:
        client.update_run(run.id, **update_payload)
    except Exception:
        return


def update_run_metrics(
    run: RunTree,
    *,
    usage_metadata: dict[str, Any] | None = None,
    first_token_time=None,
    metadata: dict[str, Any] | None = None,
    outputs: dict[str, Any] | None = None,
) -> None:
    if metadata:
        run.add_metadata(metadata)
    if outputs:
        run.add_outputs(outputs)
    if usage_metadata:
        run.set(usage_metadata=usage_metadata)
    run.patch()

    client = langsmith_client()
    if client is None:
        return

    update_payload: dict[str, Any] = {}
    if first_token_time is not None:
        update_payload["first_token_time"] = first_token_time
    if usage_metadata:
        update_payload.update(
            {
                "prompt_tokens": usage_metadata.get("input_tokens"),
                "completion_tokens": usage_metadata.get("output_tokens"),
                "total_tokens": usage_metadata.get("total_tokens"),
                "prompt_cost": usage_metadata.get("input_cost"),
                "completion_cost": usage_metadata.get("output_cost"),
                "total_cost": usage_metadata.get("total_cost"),
            }
        )
    if not update_payload:
        return
    try:
        client.update_run(run.id, **update_payload)
    except Exception:
        return


def persist_run_tree(
    run: RunTree,
    *,
    usage_metadata: dict[str, Any] | None = None,
    first_token_time=None,
) -> None:
    client = langsmith_client()
    if client is None:
        return

    payload = run._get_dicts_safe()
    if usage_metadata:
        payload.update(
            {
                "prompt_tokens": usage_metadata.get("input_tokens"),
                "completion_tokens": usage_metadata.get("output_tokens"),
                "total_tokens": usage_metadata.get("total_tokens"),
                "prompt_cost": usage_metadata.get("input_cost"),
                "completion_cost": usage_metadata.get("output_cost"),
                "total_cost": usage_metadata.get("total_cost"),
            }
        )
    if first_token_time is not None:
        payload["first_token_time"] = first_token_time
    client.create_run(**payload)


def aggregate_usage_metadata(items: list[dict[str, Any]]) -> dict[str, Any]:
    total_input_tokens = sum(int(item.get("input_tokens") or 0) for item in items)
    total_output_tokens = sum(int(item.get("output_tokens") or 0) for item in items)
    total_tokens = sum(int(item.get("total_tokens") or 0) for item in items)
    total_input_cost = sum(float(item.get("input_cost") or 0.0) for item in items)
    total_output_cost = sum(float(item.get("output_cost") or 0.0) for item in items)
    return {
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_tokens or (total_input_tokens + total_output_tokens),
        "input_cost": total_input_cost,
        "output_cost": total_output_cost,
        "total_cost": total_input_cost + total_output_cost,
    }


def earliest_timestamp(values: list[Any]):
    non_null = [value for value in values if value is not None]
    if not non_null:
        return None
    return min(non_null)


def automate_feedback(run: RunTree, result: dict[str, Any]) -> list[str]:
    if not langsmith_feedback_enabled():
        return []

    client = langsmith_client()
    if client is None:
        return []

    best_candidate = result.get("best_candidate") or {}
    scores = best_candidate.get("scores") or {}
    bundle = result.get("bundle") or {}
    plan = result.get("plan") or {}

    feedback_keys: list[str] = []
    feedback_items = [
        (
            "support",
            scores.get("support"),
            "Evidence support score from the critique node.",
        ),
        (
            "relevance",
            scores.get("relevance"),
            "Relevance score from the critique node.",
        ),
        (
            "retrieval_coverage",
            float(bool((bundle.get("jobs") or []) or (bundle.get("courses") or []))),
            "Whether the turn produced retrieved evidence.",
        ),
        (
            "response_confidence_gap",
            result.get("score_gap"),
            "Margin between the best candidate and the runner-up.",
        ),
    ]

    grounded = float(
        (scores.get("support", 0) or 0) >= 7 and not (scores.get("support_findings") or [])
    )
    feedback_items.append(
        (
            "grounded",
            grounded,
            "Heuristic groundedness flag derived from critique support findings.",
        )
    )

    for key, score, comment in feedback_items:
        if score is None:
            continue
        for attempt in range(5):
            try:
                client.create_feedback(
                    run_id=run.id,
                    trace_id=run.trace_id,
                    key=key,
                    score=score,
                    comment=comment,
                    source_info={
                        "automation": "advisor_trace_feedback",
                        "turn_id": result.get("turn_id"),
                        "intent": plan.get("intent"),
                    },
                )
                feedback_keys.append(key)
                break
            except Exception:
                if attempt == 4:
                    break
                time.sleep(1.0)

    return feedback_keys


def automate_reference_example(
    run: RunTree,
    *,
    inputs: dict[str, Any],
    result: dict[str, Any],
) -> str | None:
    if not langsmith_reference_examples_enabled():
        return None

    client = langsmith_client()
    if client is None:
        return None

    dataset = ensure_dataset(langsmith_dataset_name())
    if dataset is None:
        return None

    outputs = {
        "final_response": result.get("final_response"),
        "intent": (result.get("plan") or {}).get("intent"),
        "selected_candidate": (result.get("best_candidate") or {}).get("view", {}).get("label"),
    }
    metadata = {
        "student_id": result.get("student_id"),
        "selected_job_id": result.get("selected_job_id"),
        "score_gap": result.get("score_gap"),
        "jobs_count": len((result.get("bundle") or {}).get("jobs") or []),
        "courses_count": len((result.get("bundle") or {}).get("courses") or []),
        "source": "advisor_turn",
    }

    try:
        example = client.create_example(
            dataset_id=dataset.id,
            inputs=inputs,
            outputs=outputs,
            metadata=metadata,
            source_run_id=run.id,
            split=["reference"],
        )
        client.update_run(run.id, reference_example_id=example.id)
        return str(example.id)
    except Exception:
        return None
