from __future__ import annotations

import concurrent.futures
import operator
import os
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph
from langsmith import trace
from langsmith.run_trees import RunTree
from langsmith.run_helpers import get_current_run_tree, tracing_context

from db.supabase_client import get_supabase
from retrieval.candidates import build_candidate_views
from retrieval.context_builder import (
    build_evidence_bundle,
    get_student_profile,
)
from retrieval.critique import critique_candidate_details
from retrieval.llm import generate_candidate_details, generate_direct_response
from retrieval.observability import (
    aggregate_usage_metadata,
    attach_run_metadata,
    automate_feedback,
    automate_reference_example,
    earliest_timestamp,
    langsmith_enabled,
    langsmith_client,
    langsmith_feedback_enabled,
    langsmith_project,
    langsmith_reference_examples_enabled,
    new_trace_id,
    short_text,
    summarize_bundle,
    summarize_candidates,
    summarize_candidate_views,
    summarize_course_hits,
    summarize_job_hits,
    summarize_ranked_candidates,
    summarize_retrieval_warnings,
    summarize_student_profile,
    persist_run_tree,
    update_run_metrics,
)
from retrieval.planner import plan_retrieval
from retrieval.record_utils import job_skills_value, student_completed_courses_value, student_skill_profile_value
from retrieval.search import search_courses, search_jobs
from retrieval.skills import compute_skill_overlap, extract_skill_names, normalize_skill_name


class AdvisorState(TypedDict, total=False):
    user_message: str
    student_id: str
    selected_job_id: str | None
    session_id: str
    turn_id: str
    conversation_history: list[dict[str, str]]
    student_profile: dict[str, Any]
    plan: dict[str, Any]
    job_hits: list[dict[str, Any]]
    course_hits: list[dict[str, Any]]
    bundle: dict[str, Any]
    candidate_views: list[dict[str, Any]]
    candidates: list[dict[str, Any]]
    best_candidate: dict[str, Any]
    runner_up: dict[str, Any] | None
    score_gap: float
    final_response: str
    retrieval_refined: bool
    status_log: Annotated[list[str], operator.add]


def empty_bundle_for_student(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "student": {
            "name": profile.get("name"),
            "major": profile.get("major"),
            "skills": extract_skill_names(student_skill_profile_value(profile)),
            "completed_courses": student_completed_courses_value(profile),
        },
        "jobs": [],
        "courses": [],
    }


# Internal alias kept for graph nodes
_empty_bundle_for_student = empty_bundle_for_student


def _direct_response_text(state: AdvisorState) -> str:
    intent = state.get("plan", {}).get("intent", "general")
    profile = state.get("student_profile", {})
    return generate_direct_response(profile, state.get("user_message", ""), intent)


def _build_job_query(state: AdvisorState) -> str:
    return state["user_message"]


def _build_course_query(state: AdvisorState, job_hits: list[dict[str, Any]]) -> str:
    profile = state["student_profile"]
    student_skills = extract_skill_names(student_skill_profile_value(profile))
    missing_skills: list[str] = []
    for job in job_hits[:3]:
        if job.get("gaps"):
            missing_skills.extend(job.get("gaps", []) or [])
            continue
        required_skills = job.get("required_skills") or job.get("skills") or []
        _, gaps = compute_skill_overlap(required_skills, student_skills)
        missing_skills.extend(gaps)
    deduped_missing_skills = list(dict.fromkeys(missing_skills))
    parts = [state["user_message"]]
    if deduped_missing_skills:
        parts.append(f"Prioritize courses that teach: {', '.join(deduped_missing_skills[:12])}")
    return "\n".join(part for part in parts if part)


def _selected_job_fallback_hit(selected_job_id: str) -> dict[str, Any] | None:
    sb = get_supabase()
    job = (
        sb.table("jobs")
        .select("*")
        .eq("job_id", selected_job_id)
        .limit(1)
        .execute()
        .data
        or []
    )
    if not job:
        return None

    row = job[0]
    return {
        "job_id": row["job_id"],
        "title": row.get("title"),
        "company": row.get("company"),
        "skills": extract_skill_names(job_skills_value(row)),
        "score": 0.0,
        "semantic_score": 0.0,
        "skill_overlap": 0,
    }


def _hydrate_job_hits(job_hits: list[dict[str, Any]], student_skills: list[str]) -> list[dict[str, Any]]:
    if not job_hits:
        return []

    sb = get_supabase()
    job_ids = [hit.get("job_id") for hit in job_hits if hit.get("job_id")]
    rows = (
        sb.table("jobs")
        .select("*")
        .in_("job_id", job_ids)
        .execute()
        .data
        or []
    )
    rows_by_id = {row["job_id"]: row for row in rows if row.get("job_id")}

    hydrated_hits: list[dict[str, Any]] = []
    for hit in job_hits:
        row = rows_by_id.get(hit.get("job_id"))
        if not row:
            hydrated_hits.append(hit)
            continue
        required_skills = extract_skill_names(job_skills_value(row))
        covered, gaps = compute_skill_overlap(required_skills, student_skills)
        hydrated_hits.append({
            **hit,
            "skills": required_skills,
            "required_skills": required_skills,
            "covered": covered,
            "gaps": gaps,
        })
    return hydrated_hits


def load_student_node(state: AdvisorState) -> dict[str, Any]:
    profile = get_student_profile(state["student_id"])
    attach_run_metadata(
        metadata={
            "turn_id": state["turn_id"],
            "session_id": state["session_id"],
            "student_profile": summarize_student_profile(profile),
        },
        tags=["student", "profile"],
    )
    return {
        "student_profile": profile,
        "status_log": [f"Loaded student profile for `{profile.get('name', state['student_id'])}`."],
    }


def plan_retrieval_node(state: AdvisorState) -> dict[str, Any]:
    plan = plan_retrieval(state["user_message"], state.get("conversation_history", []))
    planner_override = False
    if state.get("selected_job_id"):
        plan["top_k_jobs"] = max(1, int(plan.get("top_k_jobs", 0)))
        reason = str(plan.get("reason", "")).strip()
        plan["reason"] = "job filter selected" if not reason else f"{reason}; job filter selected"
        planner_override = True

    attach_run_metadata(
        metadata={
            "planner": {
                "question": state["user_message"],
                "top_k_jobs": plan["top_k_jobs"],
                "top_k_courses": plan["top_k_courses"],
                "intent": plan.get("intent"),
                "reason": plan.get("reason"),
                "job_filter_override": planner_override,
                "selected_job_id": state.get("selected_job_id"),
            }
        },
        tags=["planner"],
    )

    return {
        "plan": plan,
        "status_log": [
            f"Planner selected `{plan['top_k_jobs']}` jobs and `{plan['top_k_courses']}` courses: {plan.get('reason') or 'no reason provided'}."
        ],
    }


def route_after_plan(state: AdvisorState) -> str:
    plan = state["plan"]
    if plan.get("intent") == "greeting":
        return "respond_direct"
    if plan["top_k_jobs"] == 0 and plan["top_k_courses"] == 0:
        return "respond_direct"
    return "search_jobs"


def search_jobs_node(state: AdvisorState) -> dict[str, Any]:
    plan = state["plan"]
    if plan["top_k_jobs"] <= 0:
        attach_run_metadata(
            metadata={"job_search": {"skipped": True, "reason": "planner returned zero jobs"}},
            tags=["retrieval", "jobs"],
        )
        return {"job_hits": [], "status_log": ["Skipped job search."]}

    profile = state["student_profile"]
    student_skill_names = extract_skill_names(student_skill_profile_value(profile))
    job_hits = search_jobs(
        _build_job_query(state),
        top_k=plan["top_k_jobs"],
        job_id_filter=state.get("selected_job_id"),
        student_skills=student_skill_names,
        raw_query=state["user_message"],
    )

    if not job_hits:
        if state.get("selected_job_id"):
            fallback_hit = _selected_job_fallback_hit(state["selected_job_id"])
            job_hits = [fallback_hit] if fallback_hit else []

    job_hits = _hydrate_job_hits(job_hits, student_skill_names)

    attach_run_metadata(
        metadata={
            "job_search": {
                "query": state["user_message"],
                "job_id_filter": state.get("selected_job_id"),
                "student_skills": student_skill_names,
                "fallback_used": bool(state.get("selected_job_id") and job_hits and job_hits[0]["score"] == 0.0),
                "hits": summarize_job_hits(job_hits),
            }
        },
        tags=["retrieval", "jobs"] + (["fallback"] if state.get("selected_job_id") and job_hits and job_hits[0]["score"] == 0.0 else []),
    )

    if state.get("selected_job_id") and job_hits and job_hits[0]["score"] == 0.0:
        return {
            "job_hits": job_hits,
            "status_log": [
                "Job search found no vector hit for the selected job; using the explicitly selected catalog job as the only job evidence.",
                f"[WARN] selected_job_id={state['selected_job_id']!r} had no vector match; zero-score synthetic hit used",
            ],
        }

    if not job_hits:
        return {
            "job_hits": [],
            "status_log": ["Job search returned no sufficiently relevant hits."],
        }

    return {
        "job_hits": job_hits,
        "status_log": [f"Job search returned `{len(job_hits)}` hit(s)."],
    }


def search_courses_node(state: AdvisorState) -> dict[str, Any]:
    plan = state["plan"]
    if plan["top_k_courses"] <= 0:
        attach_run_metadata(
            metadata={"course_search": {"skipped": True, "reason": "planner returned zero courses"}},
            tags=["retrieval", "courses"],
        )
        return {"course_hits": [], "status_log": ["Skipped course search."]}

    course_query = _build_course_query(state, state.get("job_hits", []))
    course_hits = search_courses(course_query, top_k=plan["top_k_courses"])
    attach_run_metadata(
        metadata={
            "course_search": {
                "query": course_query,
                "top_k_courses": plan["top_k_courses"],
                "hits": summarize_course_hits(course_hits),
            }
        },
        tags=["retrieval", "courses"],
    )
    return {
        "course_hits": course_hits,
        "status_log": [f"Course search returned `{len(course_hits)}` hit(s)."],
    }


def build_bundle_node(state: AdvisorState) -> dict[str, Any]:
    bundle = build_evidence_bundle(
        student_id=state["student_id"],
        job_hits=state.get("job_hits", []),
        course_hits=state.get("course_hits", []),
    )
    retrieval_warnings = bundle.pop("retrieval_warnings", [])
    stale_count = sum(1 for w in retrieval_warnings if w.startswith("[WARN]"))
    attach_run_metadata(
        metadata={
            "evidence_bundle": summarize_bundle(bundle),
            "stale_hit_count": stale_count,
            "retrieval_warnings": summarize_retrieval_warnings(retrieval_warnings),
        },
        tags=["evidence"] + (["stale_hits"] if stale_count > 0 else []),
    )
    log_entries = [f"Built evidence bundle with `{len(bundle['jobs'])}` jobs and `{len(bundle['courses'])}` courses."]
    log_entries.extend(retrieval_warnings)
    return {
        "bundle": bundle,
        "status_log": log_entries,
    }


def respond_direct_node(state: AdvisorState) -> dict[str, Any]:
    profile = state["student_profile"]
    bundle = _empty_bundle_for_student(profile)
    text = _direct_response_text(state)
    candidate = {
        "view": {
            "label": "Direct Response",
            "context": "",
            "evidence_description": "No retrieval required",
        },
        "text": text,
        "scores": {
            "relevance": 10,
            "support": 10,
            "utility": 8,
            "critique": "",
            "support_findings": [],
            "total": 9.2,
        },
    }
    return {
        "bundle": bundle,
        "candidate_views": [],
        "candidates": [candidate],
        "best_candidate": candidate,
        "runner_up": None,
        "score_gap": candidate["scores"]["total"],
        "final_response": text,
        "status_log": ["Answered directly without retrieval."],
    }


def build_candidate_views_node(state: AdvisorState) -> dict[str, Any]:
    views = build_candidate_views(state["bundle"])
    labels = ", ".join(view["label"] for view in views)
    attach_run_metadata(
        metadata={"candidate_views": summarize_candidate_views(views)},
        tags=["candidate-views"],
    )
    return {
        "candidate_views": views,
        "status_log": [f"Built `{len(views)}` candidate view(s): {labels}."],
    }


def _generate_candidate_branch(
    *,
    parent_run,
    state: AdvisorState,
    view: dict[str, Any],
    conversation_snapshot: list[dict[str, str]],
) -> dict[str, Any]:
    if parent_run is None:
        generation = generate_candidate_details(view["context"], conversation_snapshot, state["user_message"])
        return {
            "view": view,
            "text": generation["text"],
            "_trace_metrics": [
                {
                    "usage_metadata": generation["usage_metadata"],
                    "first_token_time": generation["first_token_time"],
                }
            ],
        }

    branch_run: RunTree = parent_run.create_child(
        name=f"candidate_branch:{view['label']}",
        run_type="llm",
        inputs={
            "label": view["label"],
            "evidence_description": view["evidence_description"],
            "context_preview": short_text(view["context"], limit=600),
            "conversation_history": conversation_snapshot[-4:],
            "user_message": state["user_message"],
        },
        tags=["advisor", "candidate", "generation", "langgraph"],
        extra={
            "metadata": {
                "turn_id": state["turn_id"],
                "session_id": state["session_id"],
                "student_id": state["student_id"],
                "selected_job_id": state.get("selected_job_id"),
                "candidate_label": view["label"],
                "graph_step": "candidate_generation",
            }
        },
    )
    with tracing_context(
        parent=branch_run,
        enabled=langsmith_enabled(),
        project_name=langsmith_project(),
    ):
        try:
            generation = generate_candidate_details(view["context"], conversation_snapshot, state["user_message"])
            text = generation["text"]
            branch_run.end(
                outputs={
                    "label": view["label"],
                    "evidence_description": view["evidence_description"],
                    "response_chars": len(text),
                    "response_preview": short_text(text, limit=600),
                    "usage_metadata": generation["usage_metadata"],
                    "timing": generation["timing_metadata"],
                }
            )
            branch_run.add_metadata(generation["metadata"])
            branch_run.add_outputs(generation["outputs"])
            branch_run.set(usage_metadata=generation["usage_metadata"])
            persist_run_tree(
                branch_run,
                usage_metadata=generation["usage_metadata"],
                first_token_time=generation["first_token_time"],
            )
            return {
                "view": view,
                "text": text,
                "_trace_metrics": [
                    {
                        "usage_metadata": generation["usage_metadata"],
                        "first_token_time": generation["first_token_time"],
                    }
                ],
            }
        except Exception as exc:
            branch_run.end(error=str(exc))
            persist_run_tree(branch_run)
            raise


def generate_candidates_node(state: AdvisorState) -> dict[str, Any]:
    conversation_snapshot = list(state.get("conversation_history", []))
    views = state["candidate_views"]
    candidates: list[dict[str, Any]] = [None] * len(views)
    parent_run = get_current_run_tree()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(views)) as executor:
        future_map = {
            executor.submit(
                _generate_candidate_branch,
                parent_run=parent_run,
                state=state,
                view=view,
                conversation_snapshot=conversation_snapshot,
            ): index
            for index, view in enumerate(views)
        }
        for future, index in future_map.items():
            candidates[index] = future.result()

    attach_run_metadata(
        metadata={"generated_candidates": summarize_candidates(candidates)},
        tags=["candidate", "generation"],
    )
    return {
        "candidates": candidates,
        "status_log": [f"Generated `{len(candidates)}` candidate response(s)."],
    }


def _critique_candidate_branch(
    *,
    parent_run,
    state: AdvisorState,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    view = candidate["view"]
    if parent_run is None:
        critique_result = critique_candidate_details(
            question=state["user_message"],
            bundle=view.get("bundle") or state["bundle"],
            context=view["context"],
            response=candidate["text"],
        )
        enriched_candidate = dict(candidate)
        enriched_candidate["scores"] = critique_result["scores"]
        existing_metrics = list(candidate.get("_trace_metrics", []))
        if critique_result.get("usage_metadata"):
            existing_metrics.append(
                {
                    "usage_metadata": critique_result["usage_metadata"],
                    "first_token_time": None,
                }
            )
        enriched_candidate["_trace_metrics"] = existing_metrics
        return enriched_candidate

    critique_run: RunTree = parent_run.create_child(
        name=f"candidate_critique:{view['label']}",
        run_type="llm",
        inputs={
            "label": view["label"],
            "evidence_description": view["evidence_description"],
            "context_preview": short_text(view["context"], limit=600),
            "candidate_response_preview": short_text(candidate["text"], limit=600),
            "question": state["user_message"],
        },
        tags=["advisor", "candidate", "critique", "langgraph"],
        extra={
            "metadata": {
                "turn_id": state["turn_id"],
                "session_id": state["session_id"],
                "student_id": state["student_id"],
                "selected_job_id": state.get("selected_job_id"),
                "candidate_label": view["label"],
                "graph_step": "candidate_critique",
            }
        },
    )
    with tracing_context(
        parent=critique_run,
        enabled=langsmith_enabled(),
        project_name=langsmith_project(),
    ):
        try:
            critique_result = critique_candidate_details(
                question=state["user_message"],
                bundle=view.get("bundle") or state["bundle"],
                context=view["context"],
                response=candidate["text"],
            )
            scores = critique_result["scores"]
            critique_run.end(outputs={"label": view["label"], "scores": scores})
            critique_run.add_metadata(
                {
                    "provider": "ollama",
                    "model": os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2"),
                    "streaming": False,
                    "ollama_timing": critique_result.get("timing_metadata"),
                    "graph_step": "candidate_critique",
                }
            )
            critique_run.add_outputs(
                {
                    "scores": scores,
                    "timing": critique_result.get("timing_metadata"),
                    "raw_response": critique_result.get("raw_response"),
                }
            )
            if critique_result.get("usage_metadata"):
                critique_run.set(usage_metadata=critique_result["usage_metadata"])
            persist_run_tree(
                critique_run,
                usage_metadata=critique_result.get("usage_metadata"),
            )
            enriched_candidate = dict(candidate)
            enriched_candidate["scores"] = scores
            existing_metrics = list(candidate.get("_trace_metrics", []))
            if critique_result.get("usage_metadata"):
                existing_metrics.append(
                    {
                        "usage_metadata": critique_result["usage_metadata"],
                        "first_token_time": None,
                    }
                )
            enriched_candidate["_trace_metrics"] = existing_metrics
            return enriched_candidate
        except Exception as exc:
            critique_run.end(error=str(exc))
            persist_run_tree(critique_run)
            raise


def critique_candidates_node(state: AdvisorState) -> dict[str, Any]:
    scored_candidates: list[dict[str, Any]] = [None] * len(state["candidates"])
    parent_run = get_current_run_tree()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(state["candidates"])) as executor:
        future_map = {
            executor.submit(
                _critique_candidate_branch,
                parent_run=parent_run,
                state=state,
                candidate=candidate,
            ): index
            for index, candidate in enumerate(state["candidates"])
        }
        for future, index in future_map.items():
            scored_candidates[index] = future.result()

    attach_run_metadata(
        metadata={"critiqued_candidates": summarize_candidates(scored_candidates)},
        tags=["candidate", "critique"],
    )
    return {
        "candidates": scored_candidates,
        "status_log": [f"Critiqued `{len(scored_candidates)}` candidate response(s)."],
    }


def select_candidate_node(state: AdvisorState) -> dict[str, Any]:
    ranked = sorted(
        state["candidates"],
        key=lambda candidate: candidate["scores"]["total"],
        reverse=True,
    )
    best_candidate = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None

    if runner_up:
        score_gap = max(0.0, best_candidate["scores"]["total"] - runner_up["scores"]["total"])
    else:
        score_gap = best_candidate["scores"]["total"]

    attach_run_metadata(
        metadata={
            "candidate_ranking": summarize_ranked_candidates(ranked),
            "selected_candidate": {
                "label": best_candidate["view"]["label"],
                "score_gap": score_gap,
                "runner_up": runner_up["view"]["label"] if runner_up else None,
                "final_response_preview": short_text(best_candidate["text"], limit=600),
            },
        },
        tags=["selection"],
    )
    return {
        "best_candidate": best_candidate,
        "runner_up": runner_up,
        "score_gap": score_gap,
        "final_response": best_candidate["text"],
        "status_log": [
            f"Selected `{best_candidate['view']['label']}` with total critique score `{best_candidate['scores']['total']}`."
        ],
    }


def _uncovered_gap_skills(bundle: dict) -> list[str]:
    """Return job gap skills that are not taught by any retrieved course."""
    gap_skills: set[str] = set()
    for job in bundle.get("jobs", []):
        for skill in job.get("gaps", []):
            if skill:
                gap_skills.add(skill)
    if not gap_skills:
        return []
    covered_by_courses: set[str] = set()
    for course in bundle.get("courses", []):
        for skill in course.get("teaches", []):
            if skill:
                covered_by_courses.add(normalize_skill_name(skill))
    return [
        skill for skill in gap_skills
        if normalize_skill_name(skill) not in covered_by_courses
    ][:8]


def refine_retrieval_node(state: AdvisorState) -> dict[str, Any]:
    """If the best candidate has low support, retrieve courses for uncovered job gaps."""
    if not state.get("candidates"):
        return {"status_log": ["Refinement skipped: no candidates."], "retrieval_refined": True}

    best = max(state["candidates"], key=lambda c: c["scores"]["total"])

    if state.get("retrieval_refined"):
        return {"status_log": ["Refinement skipped: already refined."], "retrieval_refined": True}

    if best["scores"].get("support", 10) >= 6:
        return {"status_log": ["Refinement skipped: support score sufficient."], "retrieval_refined": True}

    bundle = state.get("bundle") or {}
    targeted_skills = _uncovered_gap_skills(bundle)
    if not targeted_skills:
        return {
            "status_log": ["Refinement skipped: no uncovered gap skills in bundle."],
            "retrieval_refined": True,
        }

    targeted_query = f"courses that teach {', '.join(targeted_skills[:5])}"
    new_hits = search_courses(targeted_query, top_k=3)
    existing_ids = {c.get("course_id") for c in state.get("course_hits", [])}
    added = [h for h in new_hits if h.get("course_id") not in existing_ids]

    if not added:
        return {
            "status_log": ["Refinement: no new courses found for uncovered gap skills."],
            "retrieval_refined": True,
        }

    attach_run_metadata(
        metadata={
            "refinement": {
                "targeted_skills": targeted_skills[:5],
                "targeted_query": targeted_query,
                "added_course_hits": len(added),
            }
        },
        tags=["refinement"],
    )
    return {
        "course_hits": state.get("course_hits", []) + added,
        "retrieval_refined": True,
        "status_log": [
            f"Refinement added {len(added)} targeted course hit(s) for uncovered gaps: {', '.join(targeted_skills[:5])}."
        ],
    }


def route_after_refinement(state: AdvisorState) -> str:
    """Route to bundle rebuild if new courses were added, else go to selection."""
    if not state.get("retrieval_refined"):
        return "select_candidate"
    last_log = (state.get("status_log") or [""])[-1]
    if "Refinement added" in last_log:
        return "rebuild_bundle_refined"
    return "select_candidate"


def generate_refined_candidate_node(state: AdvisorState) -> dict[str, Any]:
    """Generate and critique one additional candidate from the refined bundle."""
    views = build_candidate_views(state["bundle"])
    if not views:
        return {"status_log": ["Refined candidate generation skipped: no views."]}
    refined_view = views[0]
    parent_run = get_current_run_tree()
    conversation_snapshot = list(state.get("conversation_history", []))
    try:
        candidate = _generate_candidate_branch(
            parent_run=parent_run,
            state=state,
            view=refined_view,
            conversation_snapshot=conversation_snapshot,
        )
        candidate["view"] = {**refined_view, "label": "Refined"}
        # Score the refined candidate so select_candidate_node can sort it.
        critique_result = _critique_candidate_branch(
            parent_run=parent_run,
            state=state,
            candidate=candidate,
        )
        existing = list(state.get("candidates", []))
        return {
            "candidates": existing + [critique_result],
            "status_log": ["Generated and critiqued 1 refined candidate from targeted course retrieval."],
        }
    except Exception:
        return {"status_log": ["Refined candidate generation/critique failed; continuing with existing candidates."]}


def build_advisor_graph():
    graph = StateGraph(AdvisorState)
    graph.add_node("load_student", load_student_node)
    graph.add_node("plan_retrieval", plan_retrieval_node)
    graph.add_node("respond_direct", respond_direct_node)
    graph.add_node("search_jobs", search_jobs_node)
    graph.add_node("search_courses", search_courses_node)
    graph.add_node("build_bundle", build_bundle_node)
    graph.add_node("build_candidate_views", build_candidate_views_node)
    graph.add_node("generate_candidates", generate_candidates_node)
    graph.add_node("critique_candidates", critique_candidates_node)
    graph.add_node("refine_retrieval", refine_retrieval_node)
    graph.add_node("rebuild_bundle_refined", build_bundle_node)
    graph.add_node("generate_refined_candidate", generate_refined_candidate_node)
    graph.add_node("select_candidate", select_candidate_node)

    graph.add_edge(START, "load_student")
    graph.add_edge("load_student", "plan_retrieval")
    graph.add_conditional_edges(
        "plan_retrieval",
        route_after_plan,
        {
            "search_jobs": "search_jobs",
            "respond_direct": "respond_direct",
        },
    )
    graph.add_edge("search_jobs", "search_courses")
    graph.add_edge("search_courses", "build_bundle")
    graph.add_edge("build_bundle", "build_candidate_views")
    graph.add_edge("build_candidate_views", "generate_candidates")
    graph.add_edge("generate_candidates", "critique_candidates")
    graph.add_edge("critique_candidates", "refine_retrieval")
    graph.add_conditional_edges(
        "refine_retrieval",
        route_after_refinement,
        {
            "select_candidate": "select_candidate",
            "rebuild_bundle_refined": "rebuild_bundle_refined",
        },
    )
    graph.add_edge("rebuild_bundle_refined", "generate_refined_candidate")
    graph.add_edge("generate_refined_candidate", "select_candidate")
    graph.add_edge("select_candidate", END)
    graph.add_edge("respond_direct", END)

    return graph.compile()


ADVISOR_GRAPH = build_advisor_graph()


def run_advisor_retrieval(
    *,
    user_message: str,
    student_id: str,
    conversation_history: list[dict[str, str]],
    selected_job_id: str | None = None,
    session_id: str | None = None,
    on_step: Any = None,
) -> dict[str, Any]:
    """
    Run planning + search + bundle building without any LLM generation or critique.
    Returns the pipeline state dict plus an `is_direct` flag.

    `on_step(message: str)` is called after each pipeline step completes so the
    caller can surface live progress (e.g. Streamlit st.write inside st.status).
    """
    resolved_session_id = session_id or new_trace_id()
    turn_id = new_trace_id()

    state: dict[str, Any] = {
        "user_message": user_message,
        "student_id": student_id,
        "selected_job_id": selected_job_id,
        "session_id": resolved_session_id,
        "turn_id": turn_id,
        "conversation_history": conversation_history or [],
        "status_log": [],
    }

    def _apply(update: dict[str, Any]) -> None:
        new_logs: list[str] = update.pop("status_log", [])
        state["status_log"].extend(new_logs)
        state.update(update)
        if on_step:
            for msg in new_logs:
                on_step(msg)

    _apply(load_student_node(state))
    _apply(plan_retrieval_node(state))

    plan = state["plan"]
    is_direct = (
        plan.get("intent") == "greeting"
        or (plan.get("top_k_jobs", 0) == 0 and plan.get("top_k_courses", 0) == 0)
    )

    if is_direct:
        return {**state, "is_direct": True}

    _apply(search_jobs_node(state))
    _apply(search_courses_node(state))

    # If retrieval returned nothing at all, fall back to direct response
    if not state.get("job_hits") and not state.get("course_hits"):
        return {**state, "is_direct": True}

    _apply(build_bundle_node(state))
    _apply(build_candidate_views_node(state))

    return {**state, "is_direct": False}


def run_advisor_turn(
    *,
    user_message: str,
    student_id: str,
    conversation_history: list[dict[str, str]],
    selected_job_id: str | None = None,
    session_id: str | None = None,
) -> AdvisorState:
    resolved_session_id = session_id or new_trace_id()
    turn_id = new_trace_id()
    initial_state: AdvisorState = {
        "user_message": user_message,
        "student_id": student_id,
        "selected_job_id": selected_job_id,
        "session_id": resolved_session_id,
        "turn_id": turn_id,
        "conversation_history": conversation_history,
        "status_log": [],
    }
    metadata = {
        "student_id": student_id,
        "selected_job_id": selected_job_id,
        "session_id": resolved_session_id,
        "turn_id": turn_id,
        "reference_examples_enabled": langsmith_reference_examples_enabled(),
        "feedback_enabled": langsmith_feedback_enabled(),
        "trace_schema_version": "v2",
    }
    invoke_config = {
        "configurable": {"thread_id": resolved_session_id},
        "metadata": metadata,
        "tags": ["advisor", "langgraph"],
    }

    final_result: AdvisorState | None = None
    root_run = RunTree(
        name="advisor_turn",
        run_type="chain",
        inputs={
            "user_message": user_message,
            "student_id": student_id,
            "selected_job_id": selected_job_id,
            "session_id": resolved_session_id,
            "conversation_length": len(conversation_history),
        },
        tags=["advisor", "langgraph"],
        extra={"metadata": metadata},
        project_name=langsmith_project(),
        ls_client=langsmith_client(),
    )

    with tracing_context(
        enabled=langsmith_enabled(),
        project_name=langsmith_project(),
        metadata=metadata,
        tags=["advisor", "langgraph"],
        parent=root_run,
    ):
        result = ADVISOR_GRAPH.invoke(initial_state, config=invoke_config)
        final_result = result
        plan = result.get("plan") or {}
        trace_metrics = [
            metric
            for candidate in result.get("candidates", [])
            for metric in candidate.get("_trace_metrics", [])
        ]
        usage_totals = aggregate_usage_metadata(
            [metric["usage_metadata"] for metric in trace_metrics if metric.get("usage_metadata")]
        )
        dynamic_tags = [
            f"intent:{plan.get('intent') or 'unknown'}",
            f"student:{student_id}",
        ]
        if selected_job_id:
            dynamic_tags.append("job-filtered")
        root_run.add_tags(dynamic_tags)
        root_run.end(
            outputs={
                "output": result.get("final_response", ""),
                "response": result.get("final_response", ""),
                "final_response": result.get("final_response", ""),
                "plan": result.get("plan"),
                "bundle": summarize_bundle(result.get("bundle", {})),
                "candidate_views": summarize_candidate_views(result.get("candidate_views", [])),
                "candidates": summarize_candidates(result.get("candidates", [])),
                "ranking": summarize_ranked_candidates(result.get("candidates", [])),
                "selected_label": result.get("best_candidate", {}).get("view", {}).get("label"),
                "runner_up_label": (
                    result.get("runner_up", {}).get("view", {}).get("label")
                    if result.get("runner_up")
                    else None
                ),
                "score_gap": result.get("score_gap"),
                "final_response_preview": short_text(result.get("final_response", ""), limit=600),
                "status_log": result.get("status_log", []),
                "usage_metadata": usage_totals,
            }
        )
    if final_result is not None:
        plan = final_result.get("plan") or {}
        trace_metrics = [
            metric
            for candidate in final_result.get("candidates", [])
            for metric in candidate.get("_trace_metrics", [])
        ]
        usage_totals = aggregate_usage_metadata(
            [metric["usage_metadata"] for metric in trace_metrics if metric.get("usage_metadata")]
        )
        first_token_time = earliest_timestamp(
            [metric.get("first_token_time") for metric in trace_metrics]
        )
        root_run.add_metadata(
            {
                "aggregated_llm_calls": len(trace_metrics),
                "graph_step": "advisor_turn",
                "intent": plan.get("intent"),
            }
        )
        root_run.add_outputs(
            {
                "output": final_result.get("final_response", ""),
                "response": final_result.get("final_response", ""),
                "final_response": final_result.get("final_response", ""),
                "final_response_preview": short_text(final_result.get("final_response", ""), limit=600),
            }
        )
        root_run.set(usage_metadata=usage_totals)
        feedback_keys = automate_feedback(root_run, {**initial_state, **final_result})
        reference_example_id = automate_reference_example(
            root_run,
            inputs={
                "user_message": user_message,
                "student_id": student_id,
                "selected_job_id": selected_job_id,
                "conversation_history": conversation_history,
            },
            result={**initial_state, **final_result},
        )
        root_run.add_metadata(
            {
                "trace_automation": {
                    "feedback_keys": feedback_keys,
                    "reference_example_id": reference_example_id,
                }
            }
        )
        persist_run_tree(root_run, usage_metadata=usage_totals, first_token_time=first_token_time)
        return final_result
    raise RuntimeError("advisor turn completed without a trace result")
