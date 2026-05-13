"""
server/api.py — FastAPI backend for the JobSkill career advisor chat.

Run:
  uvicorn api:app --reload --port 8000
"""

from __future__ import annotations

import json
import queue
import sys
import threading
from pathlib import Path
from typing import Any
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="JobSkill Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    student_id: str
    message: str
    session_id: str | None = None
    selected_job_id: str | None = None
    conversation_history: list[dict[str, str]] = []


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/api/students")
def list_students():
    from retrieval.context_builder import get_all_students
    return get_all_students()


@app.get("/api/students/{student_id}")
def get_student(student_id: str):
    from db.supabase_client import get_supabase
    from retrieval.record_utils import student_completed_courses_value, student_skill_profile_value
    from retrieval.skills import extract_skill_names
    sb = get_supabase()
    result = sb.table("students").select("*").eq("student_id", student_id).single().execute()
    row = result.data
    skills = extract_skill_names(student_skill_profile_value(row))
    courses = student_completed_courses_value(row)
    return {
        "student_id": row["student_id"],
        "name": row["name"],
        "major": row["major"],
        "skills": skills,
        "completed_courses": courses,
        "updated_at": row.get("updated_at"),
    }


@app.get("/api/jobs/locations")
def list_locations():
    """Return the top 10 cities (first segment of location string) by job count."""
    from db.supabase_client import get_supabase
    from collections import Counter
    sb = get_supabase()
    rows = sb.table("jobs").select("location").execute().data or []
    counts: Counter = Counter()
    for row in rows:
        loc = (row.get("location") or "").strip()
        city = loc.split(",")[0].strip()
        if city:
            counts[city] += 1
    top = [{"city": city, "count": cnt} for city, cnt in counts.most_common(10)]
    return top


@app.get("/api/jobs")
def list_jobs(page: int = 1, per_page: int = 10, search: str = "", location: str = ""):
    from db.supabase_client import get_supabase
    from retrieval.record_utils import job_skills_value
    from retrieval.skills import extract_skill_names
    sb = get_supabase()

    offset = (page - 1) * per_page

    query = sb.table("jobs").select(
        "job_id, title, company, location, skills_jobs_json",
        count="exact",
    )
    if search:
        query = query.ilike("title", f"%{search}%")
    if location:
        query = query.ilike("location", f"%{location}%")

    response = query.order("ingested_at", desc=True).range(offset, offset + per_page - 1).execute()
    rows = response.data or []
    total = response.count or 0

    result = []
    for row in rows:
        skills = extract_skill_names(job_skills_value(row))
        result.append({
            "job_id": row["job_id"],
            "title": row.get("title", ""),
            "company": row.get("company", ""),
            "location": row.get("location", ""),
            "top_skills": skills[:6],
        })

    return {
        "jobs": result,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, -(-total // per_page)),  # ceiling division
    }


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    from db.supabase_client import get_supabase
    from retrieval.record_utils import job_skills_value
    from retrieval.skills import extract_skill_names
    sb = get_supabase()
    result = sb.table("jobs").select("*").eq("job_id", job_id).single().execute()
    row = result.data
    skills = extract_skill_names(job_skills_value(row))
    return {
        "job_id": row["job_id"],
        "title": row.get("title", ""),
        "company": row.get("company", ""),
        "location": row.get("location", ""),
        "source": row.get("source", ""),
        "skills": skills,
        "posted_at": row.get("posted_at"),
        "ingested_at": row.get("ingested_at"),
    }


@app.post("/api/chat/stream")
async def chat_stream(body: ChatRequest):
    return StreamingResponse(
        _stream_advisor(body),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ---------------------------------------------------------------------------
# SSE helpers
# ---------------------------------------------------------------------------


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


_SENTINEL = object()


def _friendly_step(raw: str) -> str:
    """
    Convert internal log messages into human-friendly status lines.
    Falls back to the raw message if no pattern matches.
    """
    r = raw.lower()
    if "loaded student profile" in r:
        # Extract name from backtick: `Alex Chen`
        import re
        m = re.search(r"`([^`]+)`", raw)
        name = m.group(1) if m else "your profile"
        return f"Found your profile — {name}"
    if "planner selected" in r:
        import re
        jobs_m  = re.search(r"`(\d+)`\s+job", raw)
        course_m = re.search(r"`(\d+)`\s+course", raw)
        reason_m = re.search(r":\s+(.+)$", raw)
        n_jobs    = jobs_m.group(1)   if jobs_m    else "?"
        n_courses = course_m.group(1) if course_m  else "?"
        reason    = reason_m.group(1) if reason_m  else ""
        return f"Understood your question — retrieving {n_jobs} jobs & {n_courses} courses ({reason})"
    if "skipped job search" in r:
        return "No job search needed for this question"
    if "skipped course search" in r:
        return "No course search needed for this question"
    if "job search returned" in r:
        import re
        m = re.search(r"`(\d+)`", raw)
        n = m.group(1) if m else "some"
        return f"Found {n} matching job{'s' if n != '1' else ''} from 600+ postings"
    if "job search found no vector hit" in r or "no sufficiently relevant hits" in r:
        return "No strong job matches — using semantic fallback"
    if "course search returned" in r:
        import re
        m = re.search(r"`(\d+)`", raw)
        n = m.group(1) if m else "some"
        return f"Identified {n} relevant course{'s' if n != '1' else ''} for your gaps"
    if "built evidence bundle" in r:
        import re
        jobs_m   = re.search(r"`(\d+)`\s+job", raw)
        course_m = re.search(r"`(\d+)`\s+course", raw)
        n_jobs    = jobs_m.group(1)   if jobs_m    else "?"
        n_courses = course_m.group(1) if course_m  else "?"
        return f"Assembled context — {n_jobs} job{'s' if n_jobs != '1' else ''}, {n_courses} course{'s' if n_courses != '1' else ''}"
    if "built" in r and "candidate view" in r:
        return "Preparing multiple response perspectives…"
    if "generated" in r and "candidate" in r:
        return "Drafting responses from different angles…"
    if "critiqued" in r and "candidate" in r:
        return "Quality-checking each response…"
    if "selected" in r and "critique score" in r:
        import re
        m = re.search(r"score\s+`([^`]+)`", raw)
        score = m.group(1) if m else "?"
        return f"Best response selected — quality score {score}/10"
    if "answered directly" in r:
        return "Answering directly…"
    if "refinement added" in r:
        return "Refining with additional course context…"
    if "refinement skipped" in r:
        return None  # suppress noisy refinement-skip messages
    if "[warn]" in r:
        return None  # suppress internal warnings
    return raw


def _stream_advisor(body: ChatRequest):
    """
    Runs the FULL advisor graph (generate_candidates → critique_candidates → select_candidate)
    and streams results as SSE events.

    Events:
      {"type":"status","message":"..."}      — real-time node-completion updates
      {"type":"token","content":"..."}       — winning response, streamed char-by-char
      {"type":"candidates","selected":{...},"all":[...]}  — full Self-RAG comparison
      {"type":"sources","jobs":[...],"courses":[...]}
      {"type":"done"}
    """
    from retrieval.graph import ADVISOR_GRAPH
    from retrieval.observability import new_trace_id

    session_id = body.session_id or f"api-{uuid4()}"
    turn_id = new_trace_id()

    initial_state = {
        "user_message": body.message,
        "student_id": body.student_id,
        "selected_job_id": body.selected_job_id,
        "session_id": session_id,
        "turn_id": turn_id,
        "conversation_history": body.conversation_history or [],
        "status_log": [],
    }
    config = {"configurable": {"thread_id": session_id}}

    step_queue: queue.Queue = queue.Queue()
    result_box: dict = {}

    def _run_graph() -> None:
        try:
            accumulated: dict = {}
            for chunk in ADVISOR_GRAPH.stream(
                initial_state,
                config=config,
                stream_mode=["updates", "values"],
                version="v2",
            ):
                if chunk["type"] == "updates":
                    for _node, update in chunk["data"].items():
                        for raw in update.get("status_log", []):
                            msg = _friendly_step(raw)
                            if msg:
                                step_queue.put({"type": "status", "message": msg})
                elif chunk["type"] == "values":
                    accumulated = chunk["data"]

            result_box["state"] = accumulated
        except Exception as exc:
            result_box["error"] = exc
        finally:
            step_queue.put(_SENTINEL)

    # -----------------------------------------------------------------------
    # Phase 1: run the full graph, emit per-node status in real-time
    # -----------------------------------------------------------------------
    t = threading.Thread(target=_run_graph, daemon=True)
    t.start()

    while True:
        item = step_queue.get()
        if item is _SENTINEL:
            break
        yield _sse(item)

    t.join()

    if "error" in result_box:
        yield _sse({"type": "error", "message": str(result_box["error"])})
        yield _sse({"type": "done"})
        return

    state = result_box["state"]
    final_response: str = state.get("final_response", "")
    bundle: dict = state.get("bundle", {})
    candidates: list = state.get("candidates", [])
    best_candidate: dict = state.get("best_candidate", {})

    # -----------------------------------------------------------------------
    # Phase 2: stream the critique-selected winning response char-by-char
    # -----------------------------------------------------------------------
    for char in final_response:
        yield _sse({"type": "token", "content": char})

    # -----------------------------------------------------------------------
    # Phase 3: candidate comparison (the Self-RAG selection result)
    # -----------------------------------------------------------------------
    if candidates:
        all_candidates = []
        for c in candidates:
            scores = c.get("scores", {})
            label = c.get("view", {}).get("label", "?")
            evidence = c.get("view", {}).get("evidence_description", "")
            is_selected = (c is best_candidate) or (
                c.get("view", {}).get("label") == best_candidate.get("view", {}).get("label")
            )
            all_candidates.append({
                "label": label,
                "evidence": evidence,
                "total": round(scores.get("total", 0), 1),
                "relevance": scores.get("relevance", 0),
                "support": scores.get("support", 0),
                "utility": scores.get("utility", 0),
                "critique": scores.get("critique", ""),
                "selected": is_selected,
            })
        # Sort by score descending
        all_candidates.sort(key=lambda c: c["total"], reverse=True)
        selected = next((c for c in all_candidates if c["selected"]), all_candidates[0])
        yield _sse({"type": "candidates", "selected": selected, "all": all_candidates})

    # -----------------------------------------------------------------------
    # Phase 4: evidence sources
    # -----------------------------------------------------------------------
    jobs_summary = [
        {
            "title": j.get("title", ""),
            "company": j.get("company", ""),
            "score": round(j.get("score", 0), 3),
            "covered": j.get("covered", []),
            "gaps": j.get("gaps", []),
        }
        for j in bundle.get("jobs", [])
    ]
    courses_summary = [
        {
            "course_code": c.get("course_code", ""),
            "title": c.get("title", ""),
            "score": round(c.get("score", 0), 3),
            "teaches": c.get("teaches", [])[:5],
        }
        for c in bundle.get("courses", [])
    ]
    yield _sse({"type": "sources", "jobs": jobs_summary, "courses": courses_summary})

    yield _sse({"type": "done"})
