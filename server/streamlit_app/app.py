"""
streamlit_app/app.py — Student Advisor Chat (streaming)

Run:
  streamlit run streamlit_app/app.py
"""

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from dotenv import load_dotenv

from retrieval.context_builder import get_all_jobs, get_all_students, get_student_profile
from retrieval.critique import critique_candidate
from retrieval.graph import empty_bundle_for_student, run_advisor_retrieval
from retrieval.llm import stream_direct_response, stream_response
from retrieval.record_utils import student_completed_courses_value, student_skill_profile_value

load_dotenv()

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Student Advisor", layout="wide")
st.title("Student Career Advisor")


def _stop_with_error(service: str, error: Exception) -> None:
    st.error(
        f"{service} connection failed.\n\n"
        f"Error: `{error}`\n\n"
        "Please verify `.env` values and that the service is reachable, then refresh."
    )
    st.stop()


# ---------------------------------------------------------------------------
# Sidebar — student + job selection
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Session Setup")

    if "students_list" not in st.session_state:
        with st.spinner("Loading students..."):
            try:
                st.session_state.students_list = get_all_students()
            except Exception as e:
                _stop_with_error("Supabase", e)

    students = st.session_state.students_list
    student_names = {s["name"]: s["student_id"] for s in students}

    selected_name = st.selectbox("Select student", list(student_names.keys()))
    selected_student_id = student_names[selected_name]

    if st.session_state.get("active_student_id") != selected_student_id:
        st.session_state.active_student_id = selected_student_id
        with st.spinner("Loading profile..."):
            try:
                st.session_state.student_profile = get_student_profile(selected_student_id)
            except Exception as e:
                _stop_with_error("Supabase", e)
        st.session_state.conversation = []
        st.session_state.last_bundle = None
        st.session_state.advisor_session_id = f"streamlit-{uuid4()}"

    profile = st.session_state.student_profile
    st.markdown(f"**Major:** {profile.get('major', '—')}")
    completed = student_completed_courses_value(profile)
    st.markdown(f"**Courses:** {', '.join(completed) or 'none'}")
    skills = [s for s in student_skill_profile_value(profile) if isinstance(s, str)]
    st.markdown(f"**Skills:** {', '.join(skills) or 'none'}")

    st.divider()

    if "jobs_list" not in st.session_state:
        with st.spinner("Loading jobs..."):
            try:
                st.session_state.jobs_list = get_all_jobs()
            except Exception as e:
                _stop_with_error("Supabase", e)

    jobs = st.session_state.jobs_list
    job_options: dict[str, str | None] = {"Any (semantic search)": None}
    for j in jobs:
        job_options[f"{j['title']} — {j['company']}"] = j["job_id"]

    selected_job_label = st.selectbox("Job filter (optional)", list(job_options.keys()))
    selected_job_id = job_options[selected_job_label]

    st.divider()
    if st.button("Clear chat"):
        st.session_state.conversation = []
        st.session_state.last_bundle = None
        st.rerun()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "last_bundle" not in st.session_state:
    st.session_state.last_bundle = None
if "advisor_session_id" not in st.session_state:
    st.session_state.advisor_session_id = f"streamlit-{uuid4()}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pick_primary_view(views: list[dict], intent: str) -> dict:
    """Choose the most appropriate candidate view based on query intent."""
    if not views:
        raise ValueError("No candidate views to pick from")
    index_by_intent = {
        "jobs": 0,       # View A — specific job focus
        "skill_gap": 1,  # View B — all jobs for gap analysis
        "courses": 2,    # View C — course path
        "broad": 1,      # View B — most complete context
        "general": 1,    # View B — safe default
    }
    idx = index_by_intent.get(intent, 1)
    return views[min(idx, len(views) - 1)]


def _render_sources(bundle: dict) -> None:
    """Render job and course evidence inside an expander."""
    n_jobs = len(bundle.get("jobs", []))
    n_courses = len(bundle.get("courses", []))
    with st.expander(f"Evidence — {n_jobs} job{'s' if n_jobs != 1 else ''}, {n_courses} course{'s' if n_courses != 1 else ''}"):
        if bundle.get("jobs"):
            st.markdown("**Jobs retrieved:**")
            for j in bundle["jobs"]:
                gaps_str = ", ".join(j.get("gaps", [])) or "none"
                covered_str = ", ".join(j.get("covered", [])) or "none"
                st.markdown(
                    f"- **{j['title']}** @ {j['company']} "
                    f"(score: {j.get('score', 0):.3f})  \n"
                    f"  Covers: {covered_str} — Gaps: {gaps_str}"
                )
        if bundle.get("courses"):
            st.markdown("**Courses retrieved:**")
            for c in bundle["courses"]:
                teaches_str = ", ".join(c.get("teaches", [])[:5]) or "—"
                st.markdown(
                    f"- **{c['course_code']}**: {c['title']} "
                    f"(score: {c.get('score', 0):.3f})  \n"
                    f"  Teaches: {teaches_str}"
                )


def _render_scores(scores: dict) -> None:
    """Render critique scores as metrics inside an expander."""
    with st.expander("Quality Scorecard"):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Relevance", f"{scores['relevance']}/10")
        col2.metric("Support", f"{scores['support']}/10")
        col3.metric("Utility", f"{scores['utility']}/10")
        col4.metric("Total", f"{scores['total']:.1f}/10")
        if scores.get("critique"):
            st.caption(f"Critique: _{scores['critique']}_")
        if scores.get("support_findings"):
            findings = "; ".join(scores["support_findings"][:3])
            st.caption(f"Support findings: {findings}")


# ---------------------------------------------------------------------------
# Chat history — replay previous turns
# ---------------------------------------------------------------------------

for turn in st.session_state.conversation:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])
        if turn["role"] == "assistant" and turn.get("bundle"):
            _render_sources(turn["bundle"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------

user_input = st.chat_input("Ask about jobs, skills, or your learning path...")

if user_input:
    # History passed to LLM must only have role + content
    prior_history = [
        {"role": t["role"], "content": t["content"]}
        for t in st.session_state.conversation
    ]

    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # -----------------------------------------------------------------------
    # Phase 1: Retrieval — planning, search, bundle, candidate views
    # -----------------------------------------------------------------------

    retrieval_state: dict | None = None
    with st.status("Analyzing your question…", expanded=True) as retrieval_status:
        try:
            retrieval_state = run_advisor_retrieval(
                user_message=user_input,
                student_id=selected_student_id,
                selected_job_id=selected_job_id,
                conversation_history=prior_history,
                session_id=st.session_state.advisor_session_id,
                on_step=st.write,
            )
        except Exception as e:
            retrieval_status.update(label="Retrieval failed", state="error", expanded=True)
            st.error(f"Retrieval error: `{e}`")
            st.stop()

        plan = retrieval_state.get("plan", {})
        intent = plan.get("intent", "general")
        is_direct = retrieval_state.get("is_direct", False)

        if is_direct:
            retrieval_status.update(label="Ready", state="complete", expanded=False)
        else:
            views = retrieval_state.get("candidate_views", [])
            n_jobs = len(retrieval_state.get("bundle", {}).get("jobs", []))
            n_courses = len(retrieval_state.get("bundle", {}).get("courses", []))
            retrieval_status.update(
                label=f"Retrieved {n_jobs} job{'s' if n_jobs != 1 else ''}, {n_courses} course{'s' if n_courses != 1 else ''} — streaming response…",
                state="complete",
                expanded=False,
            )

    # -----------------------------------------------------------------------
    # Phase 2: Stream the response token by token
    # -----------------------------------------------------------------------

    student_profile = retrieval_state.get("student_profile", {})

    with st.chat_message("assistant"):

        if is_direct:
            # Greeting / no-evidence path
            token_iter = stream_direct_response(student_profile, user_input, intent)
            full_response: str = st.write_stream(token_iter)
            bundle = empty_bundle_for_student(student_profile)

        else:
            views = retrieval_state.get("candidate_views", [])
            bundle = retrieval_state["bundle"]

            if not views:
                # Retrieval ran but produced no views — fall back gracefully
                token_iter = stream_direct_response(student_profile, user_input, "general")
                full_response = st.write_stream(token_iter)
            else:
                best_view = _pick_primary_view(views, intent)
                st.caption(
                    f"View: **{best_view['label']}** — {best_view['evidence_description']}"
                )

                token_iter = stream_response(
                    best_view["context"], prior_history, user_input
                )
                full_response = st.write_stream(token_iter)

                # -----------------------------------------------------------
                # Phase 3: Critique + evidence (shown after streaming completes)
                # -----------------------------------------------------------

                with st.spinner("Scoring response…"):
                    try:
                        scores = critique_candidate(
                            user_input,
                            best_view.get("bundle") or bundle,
                            best_view["context"],
                            full_response,
                        )
                    except Exception:
                        scores = None

                if scores:
                    _render_scores(scores)

            _render_sources(bundle)

        st.session_state.conversation.append({
            "role": "assistant",
            "content": full_response,
            "bundle": bundle,
        })
