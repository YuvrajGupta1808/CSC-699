"""
retrieval/planner.py

Before any search, ask the LLM to decide:
  - Does this question need retrieval at all?
  - How many job results are needed? (0–10)
  - How many course results are needed? (0–10)

This replaces the hardcoded TOP_K and implements the Self-RAG
retrieve-on-demand gating step.
"""

import os
import json
import httpx
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2")

PLANNER_PROMPT = """You are a retrieval planner for a student career advisor system.

Given a user's question, decide how many job postings and course records to retrieve from the database.

Rules:
- If the question is a greeting, small talk, or needs no data → set both to 0
- If the question is about job fit, job recommendations, what roles suit the student → more jobs (5–10), few courses (0–2)
- If the question is about what to learn, which courses to take, skill gaps → few jobs (1–3), more courses (5–10)
- If the question is about a full career path, readiness, or a broad analysis → balanced (5–8 each)
- If the question targets a specific job already selected → fewer jobs needed (1–3), more courses (4–8)
- Never exceed 10 for either.

Respond ONLY with a valid JSON object, no explanation, no markdown:
{{"top_k_jobs": <int>, "top_k_courses": <int>, "reason": "<one short sentence>"}}

User question: {question}
"""


@traceable(name="plan_retrieval", run_type="llm")
def plan_retrieval(question: str) -> dict:
    """
    Returns: { "top_k_jobs": int, "top_k_courses": int, "reason": str }
    Falls back to (5, 5) if the LLM response can't be parsed.
    """
    prompt = PLANNER_PROMPT.format(question=question)
    q = question.lower()

    try:
        response = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": CHAT_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()
        raw = response.json()["message"]["content"].strip()

        # Strip markdown code fences if the model wraps the JSON
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        plan = json.loads(raw)
        # Normalize keys — LLM sometimes wraps them in extra quotes e.g. '"top_k_jobs"'
        plan = {k.strip().strip('"').strip("'"): v for k, v in plan.items()}

        top_k_jobs = max(0, min(10, int(plan.get("top_k_jobs", 5))))
        top_k_courses = max(0, min(10, int(plan.get("top_k_courses", 5))))

        # Deterministic guardrails so obvious intent never returns zero retrieval.
        asks_for_jobs = any(k in q for k in ["job", "jobs", "role", "roles", "position", "intern"])
        asks_for_courses = any(k in q for k in ["course", "courses", "learn", "learning", "skill gap", "upskill"])
        if asks_for_jobs:
            top_k_jobs = max(top_k_jobs, 5)
        if asks_for_courses:
            top_k_courses = max(top_k_courses, 4)
        reason = str(plan.get("reason", ""))
        return {"top_k_jobs": top_k_jobs, "top_k_courses": top_k_courses, "reason": reason}

    except Exception:
        # Use intent-aware defaults on parser/network failures.
        asks_for_jobs = any(k in q for k in ["job", "jobs", "role", "roles", "position", "intern"])
        asks_for_courses = any(k in q for k in ["course", "courses", "learn", "learning", "skill gap", "upskill"])
        return {
            "top_k_jobs": 5 if asks_for_jobs else 3,
            "top_k_courses": 5 if asks_for_courses else 3,
            "reason": "fallback defaults",
        }
