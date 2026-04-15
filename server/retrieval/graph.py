from __future__ import annotations

import concurrent.futures
import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph
from langsmith import trace
from langsmith.run_helpers import get_current_run_tree, tracing_context

from retrieval.candidates import build_candidate_views
from retrieval.context_builder import (
    build_evidence_bundle,
    get_all_jobs,
    get_student_profile,
)
from retrieval.critique import critique_candidate
from retrieval.llm import generate_candidate
from retrieval.observability import (
    attach_run_metadata,
    langsmith_enabled,
    langsmith_project,
    new_trace_id,
    short_text,
    summarize_bundle,
    summarize_candidates,
    summarize_candidate_views,
    summarize_course_hits,
    summarize_job_hits,
    summarize_ranked_candidates,
    summarize_student_profile,
)
from retrieval.planner import plan_retrieval
from retrieval.search import search_courses, search_jobs


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
    status_log: Annotated[list[str], operator.add]


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
    plan = plan_retrieval(state["user_message"])
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
    if plan["top_k_jobs"] == 0 and plan["top_k_courses"] == 0:
        return "build_bundle"
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
    student_skill_names = [
        s["skill"]
        for s in (profile.get("skill_profile_json") or [])
        if isinstance(s, dict) and s.get("skill")
    ]
    job_hits = search_jobs(
        state["user_message"],
        top_k=plan["top_k_jobs"],
        job_id_filter=state.get("selected_job_id"),
        student_skills=student_skill_names,
    )

    fallback_used = False
    if not job_hits:
        all_jobs = get_all_jobs()
        if state.get("selected_job_id"):
            fallback_jobs = [j for j in all_jobs if j.get("job_id") == state["selected_job_id"]]
        else:
            fallback_jobs = all_jobs[: max(3, plan["top_k_jobs"])]
        job_hits = [
            {
                "job_id": j["job_id"],
                "title": j["title"],
                "company": j["company"],
                "skills": [],
                "score": 0.0,
            }
            for j in fallback_jobs
        ]
        fallback_used = True

    attach_run_metadata(
        metadata={
            "job_search": {
                "query": state["user_message"],
                "job_id_filter": state.get("selected_job_id"),
                "student_skills": student_skill_names,
                "fallback_used": fallback_used,
                "hits": summarize_job_hits(job_hits),
            }
        },
        tags=["retrieval", "jobs"] + (["fallback"] if fallback_used else []),
    )

    if fallback_used:
        return {
            "job_hits": job_hits,
            "status_log": [f"Job search found no vector hits; fallback returned `{len(job_hits)}` catalog job(s)."],
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

    course_hits = search_courses(state["user_message"], top_k=plan["top_k_courses"])
    attach_run_metadata(
        metadata={
            "course_search": {
                "query": state["user_message"],
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
    attach_run_metadata(
        metadata={"evidence_bundle": summarize_bundle(bundle)},
        tags=["evidence"],
    )
    return {
        "bundle": bundle,
        "status_log": [
            f"Built evidence bundle with `{len(bundle['jobs'])}` jobs and `{len(bundle['courses'])}` courses."
        ],
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
    with tracing_context(
        parent=parent_run,
        enabled=langsmith_enabled(),
        project_name=langsmith_project(),
    ):
        with trace(
            name=f"candidate_branch:{view['label']}",
            run_type="chain",
            inputs={
                "label": view["label"],
                "evidence_description": view["evidence_description"],
                "context_preview": short_text(view["context"], limit=600),
                "conversation_history": conversation_snapshot[-4:],
                "user_message": state["user_message"],
            },
            metadata={
                "turn_id": state["turn_id"],
                "session_id": state["session_id"],
                "student_id": state["student_id"],
                "selected_job_id": state.get("selected_job_id"),
            },
            tags=["candidate", "generation"],
        ) as run:
            text = generate_candidate(view["context"], conversation_snapshot, state["user_message"])
            run.end(
                outputs={
                    "label": view["label"],
                    "evidence_description": view["evidence_description"],
                    "response_chars": len(text),
                    "response_preview": short_text(text, limit=600),
                }
            )
            run.patch()
            return {"view": view, "text": text}


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
    with tracing_context(
        parent=parent_run,
        enabled=langsmith_enabled(),
        project_name=langsmith_project(),
    ):
        with trace(
            name=f"candidate_critique:{view['label']}",
            run_type="chain",
            inputs={
                "label": view["label"],
                "evidence_description": view["evidence_description"],
                "context_preview": short_text(view["context"], limit=600),
                "candidate_response_preview": short_text(candidate["text"], limit=600),
                "question": state["user_message"],
            },
            metadata={
                "turn_id": state["turn_id"],
                "session_id": state["session_id"],
                "student_id": state["student_id"],
                "selected_job_id": state.get("selected_job_id"),
            },
            tags=["candidate", "critique"],
        ) as run:
            scores = critique_candidate(state["user_message"], view["context"], candidate["text"])
            run.end(outputs={"label": view["label"], "scores": scores})
            run.patch()
            enriched_candidate = dict(candidate)
            enriched_candidate["scores"] = scores
            return enriched_candidate


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
    ranked = sorted(state["candidates"], key=lambda candidate: candidate["scores"]["total"], reverse=True)
    best_candidate = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None
    score_gap = (
        best_candidate["scores"]["total"] - runner_up["scores"]["total"]
        if runner_up
        else best_candidate["scores"]["total"]
    )
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


def build_advisor_graph():
    graph = StateGraph(AdvisorState)
    graph.add_node("load_student", load_student_node)
    graph.add_node("plan_retrieval", plan_retrieval_node)
    graph.add_node("search_jobs", search_jobs_node)
    graph.add_node("search_courses", search_courses_node)
    graph.add_node("build_bundle", build_bundle_node)
    graph.add_node("build_candidate_views", build_candidate_views_node)
    graph.add_node("generate_candidates", generate_candidates_node)
    graph.add_node("critique_candidates", critique_candidates_node)
    graph.add_node("select_candidate", select_candidate_node)

    graph.add_edge(START, "load_student")
    graph.add_edge("load_student", "plan_retrieval")
    graph.add_conditional_edges(
        "plan_retrieval",
        route_after_plan,
        {
            "search_jobs": "search_jobs",
            "build_bundle": "build_bundle",
        },
    )
    graph.add_edge("search_jobs", "search_courses")
    graph.add_edge("search_courses", "build_bundle")
    graph.add_edge("build_bundle", "build_candidate_views")
    graph.add_edge("build_candidate_views", "generate_candidates")
    graph.add_edge("generate_candidates", "critique_candidates")
    graph.add_edge("critique_candidates", "select_candidate")
    graph.add_edge("select_candidate", END)

    return graph.compile()


ADVISOR_GRAPH = build_advisor_graph()


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
    }
    invoke_config = {
        "configurable": {"thread_id": resolved_session_id},
        "metadata": metadata,
        "tags": ["advisor", "langgraph"],
    }

    with tracing_context(
        enabled=langsmith_enabled(),
        project_name=langsmith_project(),
        metadata=metadata,
        tags=["advisor", "langgraph"],
    ):
        with trace(
            name="advisor_turn",
            run_type="chain",
            inputs={
                "user_message": user_message,
                "student_id": student_id,
                "selected_job_id": selected_job_id,
                "session_id": resolved_session_id,
                "conversation_length": len(conversation_history),
            },
            metadata=metadata,
            tags=["advisor", "langgraph"],
        ) as run:
            result = ADVISOR_GRAPH.invoke(initial_state, config=invoke_config)
            run.end(
                outputs={
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
                }
            )
            run.patch()
            return result
