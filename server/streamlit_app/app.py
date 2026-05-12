"""
streamlit_app/app.py — Student Advisor Chat

Run:
  streamlit run streamlit_app/app.py
"""

import sys
from pathlib import Path
from uuid import uuid4

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from dotenv import load_dotenv

from retrieval.context_builder import (
    get_all_students,
    get_all_jobs,
    get_student_profile,
)
from retrieval.graph import run_advisor_turn
from retrieval.record_utils import student_completed_courses_value, student_skill_profile_value

load_dotenv()


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Student Advisor", layout="wide")
st.title("Student Career Advisor")


def stop_with_config_error(service: str, error: Exception):
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

    # Load students once
    if "students_list" not in st.session_state:
        with st.spinner("Loading students..."):
            try:
                st.session_state.students_list = get_all_students()
            except Exception as e:
                stop_with_config_error("Supabase", e)

    students = st.session_state.students_list
    student_names = {s["name"]: s["student_id"] for s in students}

    selected_name = st.selectbox("Select student", list(student_names.keys()))
    selected_student_id = student_names[selected_name]

    # Reload profile when student changes
    if st.session_state.get("active_student_id") != selected_student_id:
        st.session_state.active_student_id = selected_student_id
        with st.spinner("Loading profile..."):
            try:
                st.session_state.student_profile = get_student_profile(selected_student_id)
            except Exception as e:
                stop_with_config_error("Supabase", e)
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

    # Optional job filter
    if "jobs_list" not in st.session_state:
        with st.spinner("Loading jobs..."):
            try:
                st.session_state.jobs_list = get_all_jobs()
            except Exception as e:
                stop_with_config_error("Supabase", e)

    jobs = st.session_state.jobs_list
    job_options = {"Any (semantic search)": None}
    for j in jobs:
        label = f"{j['title']} — {j['company']}"
        job_options[label] = j["job_id"]

    selected_job_label = st.selectbox("Job filter (optional)", list(job_options.keys()))
    selected_job_id = job_options[selected_job_label]

    st.divider()
    if st.button("Clear chat"):
        st.session_state.conversation = []
        st.session_state.last_bundle = None
        st.rerun()

# ---------------------------------------------------------------------------
# Initialize session state
# ---------------------------------------------------------------------------

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "last_bundle" not in st.session_state:
    st.session_state.last_bundle = None
if "advisor_session_id" not in st.session_state:
    st.session_state.advisor_session_id = f"streamlit-{uuid4()}"

# ---------------------------------------------------------------------------
# Chat history display
# ---------------------------------------------------------------------------

for turn in st.session_state.conversation:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])
        if turn["role"] == "assistant" and turn.get("bundle"):
            bundle = turn["bundle"]
            with st.expander(f"Sources — {len(bundle['jobs'])} jobs, {len(bundle['courses'])} courses"):
                if bundle["jobs"]:
                    st.markdown("**Jobs retrieved:**")
                    for j in bundle["jobs"]:
                        gaps_str = ", ".join(j.get("gaps", [])) or "none"
                        st.markdown(
                            f"- **{j['title']}** at {j['company']} "
                            f"(score: {j['score']}) — gaps: {gaps_str}"
                        )
                if bundle["courses"]:
                    st.markdown("**Courses retrieved:**")
                    for c in bundle["courses"]:
                        st.markdown(f"- **{c['course_code']}**: {c['title']} (score: {c['score']})")

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------

user_input = st.chat_input("Ask about jobs, skills, or your learning path...")

if user_input:
    prior_conversation = list(st.session_state.conversation)

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.conversation.append({"role": "user", "content": user_input})

    with st.status("Running LangGraph advisor workflow...", expanded=True) as status:
        try:
            result = run_advisor_turn(
                user_message=user_input,
                student_id=selected_student_id,
                selected_job_id=selected_job_id,
                conversation_history=prior_conversation,
                session_id=st.session_state.advisor_session_id,
            )
        except Exception as e:
            status.update(label="LangGraph advisor workflow failed", state="error", expanded=True)
            st.error(f"Advisor workflow failed.\n\nError: `{e}`")
            st.stop()

        for line in result.get("status_log", []):
            st.write(line)

        status.update(label="LangGraph advisor workflow complete", state="complete", expanded=False)

    # --- Render the winning candidate ---
    with st.chat_message("assistant"):
        best = result["best_candidate"]
        runner_up = result.get("runner_up")
        score_gap = result.get("score_gap", 999.0)
        bundle = result["bundle"]
        candidates = result["candidates"]
        full_response = result["final_response"]
        st.session_state.last_bundle = bundle

        st.caption(f"Selected: **{best['view']['label']}** — {best['view']['evidence_description']}")

        # If scores are very close, offer the runner-up as an alternative
        if runner_up and score_gap < 1.0:
            st.caption(
                f"Runner-up: **{runner_up['view']['label']}** (score {runner_up['scores']['total']}) — "
                f"close match, shown in expander below."
            )

        st.markdown(full_response)

        # Critique scorecard
        with st.expander("Self-RAG Critique Scorecard"):
            for c in sorted(candidates, key=lambda x: x["scores"]["total"], reverse=True):
                sc = c["scores"]
                marker = " ← selected" if c is best else ""
                st.markdown(
                    f"**{c['view']['label']}**{marker} — "
                    f"R:`{sc['relevance']}` S:`{sc['support']}` U:`{sc['utility']}` "
                    f"total:`{sc['total']}`  \n_{sc['critique']}_"
                )
                if sc.get("support_findings"):
                    st.caption("Support checks: " + "; ".join(sc["support_findings"]))
            if runner_up and score_gap < 1.0:
                st.markdown("---")
                st.markdown(f"**Runner-up ({runner_up['view']['label']}) full response:**")
                st.markdown(runner_up["text"])

        # Sources
        with st.expander(f"Evidence — {len(bundle['jobs'])} jobs, {len(bundle['courses'])} courses"):
            if bundle["jobs"]:
                st.markdown("**Jobs:**")
                for j in bundle["jobs"]:
                    gaps_str = ", ".join(j.get("gaps", [])) or "none"
                    st.markdown(f"- **{j['title']}** @ {j['company']} (score: {j['score']}) — gaps: {gaps_str}")
            if bundle["courses"]:
                st.markdown("**Courses:**")
                for c in bundle["courses"]:
                    st.markdown(f"- **{c['course_code']}**: {c['title']} (score: {c['score']})")

    st.session_state.conversation.append({
        "role": "assistant",
        "content": full_response,
        "bundle": bundle,
    })
