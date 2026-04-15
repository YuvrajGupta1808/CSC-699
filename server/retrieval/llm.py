import json
import os
from collections.abc import Iterator

import httpx
from dotenv import load_dotenv
from langsmith import traceable

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


def build_chat_messages(context: str, history: list[dict], user_message: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context}]
    for turn in history[-4:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages


@traceable(name="generate_candidate", run_type="llm")
def generate_candidate(context: str, history: list[dict], user_message: str) -> str:
    """Non-streaming Ollama chat call."""
    resp = httpx.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": CHAT_MODEL, "messages": build_chat_messages(context, history, user_message), "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def stream_response(context: str, history: list[dict], user_message: str) -> Iterator[str]:
    """Stream tokens from Ollama chat endpoint."""
    with httpx.stream(
        "POST",
        f"{OLLAMA_URL}/api/chat",
        json={"model": CHAT_MODEL, "messages": build_chat_messages(context, history, user_message), "stream": True},
        timeout=120,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            token = chunk.get("message", {}).get("content", "")
            if token:
                yield token
            if chunk.get("done"):
                break
