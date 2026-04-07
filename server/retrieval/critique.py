"""
retrieval/critique.py

Scores each generated candidate on 3 axes from the Self-RAG paper:
  Relevance  — does it answer the user's actual question?
  Support    — are claims traceable to the evidence provided?
  Utility    — is the answer actionable with concrete next steps?

Each axis scored 0–10. Final score = weighted sum.
"""

import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2")

CRITIQUE_PROMPT = """You are a critic evaluating an AI advisor's response to a student career question.

Score the response on exactly these 3 axes (0–10 each):

- relevance: Does the response directly answer the student's question without drifting off-topic?
- support: Are the specific claims (job names, skill names, course codes) traceable to the evidence context? No hallucinated facts?
- utility: Is the response actionable? Does it give concrete skill gaps, course recommendations, or next steps — not vague advice?

STUDENT QUESTION:
{question}

EVIDENCE CONTEXT USED:
{context}

RESPONSE TO CRITIQUE:
{response}

Respond ONLY with valid JSON, no explanation, no markdown:
{{"relevance": <int>, "support": <int>, "utility": <int>, "critique": "<one sentence on the weakest axis>"}}
"""


def critique_candidate(question: str, context: str, response: str) -> dict:
    """
    Returns: { "relevance": int, "support": int, "utility": int,
               "critique": str, "total": float }
    Falls back to (5,5,5) if parsing fails.
    """
    prompt = CRITIQUE_PROMPT.format(
        question=question,
        context=context[:1500],   # trim context to avoid token overload
        response=response[:1000],
    )

    try:
        resp = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": CHAT_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=45,
        )
        resp.raise_for_status()
        raw = resp.json()["message"]["content"].strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        scores = json.loads(raw)
        # Normalize keys — LLM sometimes wraps them in extra quotes
        scores = {k.strip().strip('"').strip("'"): v for k, v in scores.items()}
        r = max(0, min(10, int(scores.get("relevance", 5))))
        s = max(0, min(10, int(scores.get("support", 5))))
        u = max(0, min(10, int(scores.get("utility", 5))))
        # Weighted: support matters most (grounding), then utility, then relevance
        total = round(s * 0.4 + u * 0.4 + r * 0.2, 2)
        return {
            "relevance": r,
            "support": s,
            "utility": u,
            "critique": scores.get("critique", ""),
            "total": total,
        }

    except Exception:
        return {"relevance": 5, "support": 5, "utility": 5, "critique": "parse error", "total": 5.0}
