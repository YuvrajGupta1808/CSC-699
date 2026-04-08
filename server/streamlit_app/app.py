"""
streamlit_app/app.py — Student Advisor Chat

Run:
  streamlit run streamlit_app/app.py
"""

import sys
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import json
import httpx
import concurrent.futures
import streamlit as st
from dotenv import load_dotenv

from retrieval.context_builder import (
    get_all_students,
    get_all_jobs,
    get_student_profile,
    build_evidence_bundle,
    bundle_to_context_string,
)
from retrieval.search import search_jobs, search_courses
from retrieval.planner import plan_retrieval
from retrieval.candidates import build_candidate_views
from retrieval.critique import critique_candidate

load_dotenv()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2")

SYSTEM_PROMPT = """You are a personalized career advisor for CS students.
You are the advisor, not the student.
Always address the student as "you" and never role-play as the student.
Never use first-person student statements such as "I completed..." or "my skills are...".
Answer only using the evidence provided in the context below.
Be specific: reference exact job titles, skill names, and course codes.
Never invent job titles, companies, course codes, or skills that are not present in the evidence.
When listing roles, only use exact job titles from the retrieved evidence.
If the context does not contain enough information to answer, say so clearly."""


# ---------------------------------------------------------------------------
# LLM call (streaming)
# ---------------------------------------------------------------------------

def generate_candidate(context: str, history: list[dict], user_message: str) -> str:
    """Non-streaming generation — used for parallel candidates."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context}]
    for turn in history[-4:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})

    resp = httpx.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": CHAT_MODEL, "messages": messages, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def stream_response(context: str, history: list[dict], user_message: str):
    """Stream tokens from Ollama chat endpoint."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context}]
    # Include last 4 turns for continuity
    for turn in history[-4:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})

    with httpx.stream(
        "POST",
        f"{OLLAMA_URL}/api/chat",
        json={"model": CHAT_MODEL, "messages": messages, "stream": True},
        timeout=120,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            import json
            chunk = json.loads(line)
            token = chunk.get("message", {}).get("content", "")
            if token:
                yield token
            if chunk.get("done"):
                break


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Student Advisor", layout="wide")
st.title("Student Career Advisor")

# ---------------------------------------------------------------------------
# Sidebar — student + job selection
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Session Setup")

    # Load students once
    if "students_list" not in st.session_state:
        with st.spinner("Loading students..."):
            st.session_state.students_list = get_all_students()

    students = st.session_state.students_list
    student_names = {s["name"]: s["student_id"] for s in students}

    selected_name = st.selectbox("Select student", list(student_names.keys()))
    selected_student_id = student_names[selected_name]

    # Reload profile when student changes
    if st.session_state.get("active_student_id") != selected_student_id:
        st.session_state.active_student_id = selected_student_id
        with st.spinner("Loading profile..."):
            st.session_state.student_profile = get_student_profile(selected_student_id)
        st.session_state.conversation = []
        st.session_state.last_bundle = None

    profile = st.session_state.student_profile
    st.markdown(f"**Major:** {profile.get('major', '—')}")
    completed = profile.get("completed_courses_json") or []
    st.markdown(f"**Courses:** {', '.join(completed) or 'none'}")
    skills = [s["skill"] for s in (profile.get("skill_profile_json") or [])]
    st.markdown(f"**Skills:** {', '.join(skills) or 'none'}")

    st.divider()

    # Optional job filter
    if "jobs_list" not in st.session_state:
        with st.spinner("Loading jobs..."):
            st.session_state.jobs_list = get_all_jobs()

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
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # --- Retrieval pipeline with live status log ---
    with st.status("Running retrieval pipeline...", expanded=True) as status:

        st.write("Planning retrieval strategy...")
        plan = plan_retrieval(user_input)
        # If the user explicitly selects a job in the filter, always retrieve that job.
        # This prevents planner mistakes from skipping retrieval for "why this job..." questions.
        if selected_job_id:
            plan["top_k_jobs"] = max(1, int(plan.get("top_k_jobs", 0)))
            if not plan.get("reason"):
                plan["reason"] = "job filter selected"
            elif "job filter selected" not in plan["reason"].lower():
                plan["reason"] = f"{plan['reason']}; job filter selected"
        st.write(
            f"Strategy: `{plan['top_k_jobs']}` jobs, `{plan['top_k_courses']}` courses "
            f"— _{plan['reason']}_"
        )

        if plan["top_k_jobs"] == 0 and plan["top_k_courses"] == 0:
            st.write("No retrieval needed for this question.")
            job_hits, course_hits = [], []
        else:
            if plan["top_k_jobs"] > 0:
                st.write(f"Embedding query + searching `jobs_collection` (top {plan['top_k_jobs']})...")
                student_skill_names = [s["skill"] for s in (profile.get("skill_profile_json") or []) if s.get("skill")]
                job_hits = search_jobs(
                    user_input,
                    top_k=plan["top_k_jobs"],
                    job_id_filter=selected_job_id,
                    student_skills=student_skill_names,
                )
                if job_hits:
                    for j in job_hits:
                        st.write(
                            f"  • **{j['title']}** @ {j['company']} "
                            f"(score: `{j['score']}`, semantic: `{j.get('semantic_score', j['score'])}`, "
                            f"skill-overlap: `{j.get('skill_overlap', 0)}`)"
                        )
                else:
                    st.write("No semantic job hits found; using fallback catalog retrieval...")
                    all_jobs = st.session_state.get("jobs_list") or []
                    if selected_job_id:
                        fallback_jobs = [j for j in all_jobs if j.get("job_id") == selected_job_id]
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

                    if job_hits:
                        st.write(f"Fallback returned `{len(job_hits)}` job posting(s) from Supabase.")
                    else:
                        st.write("No jobs found in Supabase. Run `python ingest.py` to seed job postings.")
            else:
                st.write("Skipping job search (not needed).")
                job_hits = []

            if plan["top_k_courses"] > 0:
                st.write(f"Searching `courses_collection` (top {plan['top_k_courses']})...")
                course_hits = search_courses(user_input, top_k=plan["top_k_courses"])
                for c in course_hits:
                    st.write(f"  • **{c['course_code']}**: {c['title']} (score: `{c['score']}`)")
            else:
                st.write("Skipping course search (not needed).")
                course_hits = []

        st.write("Fetching full rows from Supabase + computing skill gaps...")
        bundle = build_evidence_bundle(
            student_id=selected_student_id,
            job_hits=job_hits,
            course_hits=course_hits,
        )

        # Log skill gaps per job
        for j in bundle["jobs"]:
            gaps = j.get("gaps", [])
            covered = j.get("covered", [])
            st.write(
                f"  **{j['title']}** — covered: `{len(covered)}` skills | "
                f"gaps: `{', '.join(gaps) or 'none'}`"
            )

        st.session_state.last_bundle = bundle

        # Build 3 evidence views
        views = build_candidate_views(bundle)
        st.write(f"Built `{len(views)}` parallel evidence views:")
        for v in views:
            st.write(f"  • **{v['label']}** — {v['evidence_description']}")

        status.update(label="Retrieval complete — generating 3 parallel candidates", state="running", expanded=False)

    # --- Parallel generation ---
    # Capture conversation snapshot before threads — st.session_state is not thread-safe
    conversation_snapshot = list(st.session_state.conversation)

    with st.status("Generating 3 candidates in parallel...", expanded=True) as gen_status:
        def _generate(view):
            return generate_candidate(view["context"], conversation_snapshot, user_input)

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(_generate, v): v for v in views}
            candidates = []
            for future, view in futures.items():
                text = future.result()
                candidates.append({"view": view, "text": text})
                st.write(f"  ✓ **{view['label']}** generated ({len(text)} chars)")

        gen_status.update(label="3 candidates generated — critiquing", state="running", expanded=False)

    # --- Critique in parallel ---
    with st.status("Critiquing candidates (Relevance · Support · Utility)...", expanded=True) as crit_status:
        def _critique(c):
            return critique_candidate(user_input, c["view"]["context"], c["text"])

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(_critique, c): c for c in candidates}
            for future, c in futures.items():
                scores = future.result()
                c["scores"] = scores
                st.write(
                    f"  **{c['view']['label']}** — "
                    f"R:`{scores['relevance']}` S:`{scores['support']}` U:`{scores['utility']}` "
                    f"→ total `{scores['total']}` | _{scores['critique']}_"
                )

        # Select best
        best = max(candidates, key=lambda c: c["scores"]["total"])
        runner_up = sorted(candidates, key=lambda c: c["scores"]["total"], reverse=True)[1]
        score_gap = best["scores"]["total"] - runner_up["scores"]["total"]

        crit_status.update(
            label=f"Selected: {best['view']['label']} (score {best['scores']['total']})",
            state="complete",
            expanded=False,
        )

    # --- Stream the winning candidate ---
    with st.chat_message("assistant"):
        st.caption(f"Selected: **{best['view']['label']}** — {best['view']['evidence_description']}")

        # If scores are very close, offer the runner-up as an alternative
        if score_gap < 1.0:
            st.caption(
                f"Runner-up: **{runner_up['view']['label']}** (score {runner_up['scores']['total']}) — "
                f"close match, shown in expander below."
            )

        response_placeholder = st.empty()
        full_response = ""
        for token in stream_response(best["view"]["context"], st.session_state.conversation, user_input):
            full_response += token
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

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
            if score_gap < 1.0:
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
