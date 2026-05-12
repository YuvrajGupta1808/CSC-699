import json
import os
import re
from collections.abc import Iterator
from datetime import datetime, timezone
from time import perf_counter

import httpx
from dotenv import load_dotenv
from retrieval.observability import ollama_timing_metadata, ollama_usage_metadata, short_text
from retrieval.prompts import GREETING_PROMPT, NO_EVIDENCE_PROMPT, SYSTEM_PROMPT

load_dotenv()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2")


def build_chat_messages(context: str, history: list[dict], user_message: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context}]
    for turn in history[-4:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages


def generate_candidate_details(context: str, history: list[dict], user_message: str) -> dict:
    """Stream an Ollama chat call and return response plus observability details."""
    messages = build_chat_messages(context, history, user_message)
    request_started_at = datetime.now(timezone.utc)
    request_started_clock = perf_counter()
    first_token_time = None
    response_payload: dict = {}
    chunks: list[str] = []
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
            chunk = json.loads(line)
            token = chunk.get("message", {}).get("content", "")
            if token:
                if first_token_time is None:
                    first_token_time = datetime.now(timezone.utc)
                chunks.append(token)
            if chunk.get("done"):
                response_payload = chunk
                break

    text = "".join(chunks).strip()
    usage_metadata = ollama_usage_metadata(response_payload)
    timing_metadata = ollama_timing_metadata(response_payload)
    metadata = {
        "provider": "ollama",
        "model": CHAT_MODEL,
        "streaming": True,
        "history_turns": len(history[-4:]),
        "context_chars": len(context or ""),
        "first_token_seconds": (
            round((first_token_time - request_started_at).total_seconds(), 6)
            if first_token_time is not None
            else None
        ),
        "wall_clock_seconds": round(perf_counter() - request_started_clock, 6),
        "ollama_timing": timing_metadata,
        "finish_reason": response_payload.get("done_reason"),
    }
    outputs = {
        "response": text,
        "response_preview": short_text(text, limit=600),
        "usage_metadata": usage_metadata,
        "timing": timing_metadata,
        "done_reason": response_payload.get("done_reason"),
        "created_at": response_payload.get("created_at"),
    }
    return {
        "text": text,
        "usage_metadata": usage_metadata,
        "timing_metadata": timing_metadata,
        "metadata": metadata,
        "outputs": outputs,
        "first_token_time": first_token_time,
    }


def generate_candidate(context: str, history: list[dict], user_message: str) -> str:
    return generate_candidate_details(context, history, user_message)["text"]


def _fallback_direct_response(intent: str) -> str:
    if intent == "greeting":
        return "Hi! I can help match jobs to your profile, identify skill gaps, and recommend specific courses. What would you like to explore?"
    return "I need a more specific question to give you a reliable answer — try asking about a target job role, a skill you want to build, or a course recommendation."


def generate_direct_response(student_profile: dict, user_message: str, intent: str) -> str:
    """Generate a greeting or no-evidence response via LLM (no hardcoded text)."""
    student_name = student_profile.get("name", "there")
    student_major = student_profile.get("major", "Computer Science")

    if intent == "greeting":
        prompt = GREETING_PROMPT.format(
            student_name=student_name,
            student_major=student_major,
            user_message=user_message,
        )
    else:
        prompt = NO_EVIDENCE_PROMPT.format(
            student_name=student_name,
            student_major=student_major,
            user_message=user_message,
        )

    try:
        resp = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": CHAT_MODEL, "messages": [{"role": "user", "content": prompt}], "stream": False},
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["message"]["content"].strip()
        raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        return raw if raw else _fallback_direct_response(intent)
    except Exception:
        return _fallback_direct_response(intent)


def _filter_think_blocks(tokens: Iterator[str]) -> Iterator[str]:
    """Strip <think>...</think> blocks from a live token stream."""
    buffer = ""
    in_think = False
    for token in tokens:
        buffer += token
        while True:
            if in_think:
                end = buffer.find("</think>")
                if end >= 0:
                    buffer = buffer[end + len("</think>"):]
                    in_think = False
                else:
                    buffer = ""
                    break
            else:
                start = buffer.find("<think>")
                if start >= 0:
                    if start > 0:
                        yield buffer[:start]
                    buffer = buffer[start + len("<think>"):]
                    in_think = True
                else:
                    safe_len = max(0, len(buffer) - 7)
                    if safe_len > 0:
                        yield buffer[:safe_len]
                        buffer = buffer[safe_len:]
                    break
    if buffer and not in_think:
        yield buffer


def _raw_token_stream(messages: list[dict]) -> Iterator[str]:
    """Low-level token iterator from Ollama."""
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
            chunk = json.loads(line)
            token = chunk.get("message", {}).get("content", "")
            if token:
                yield token
            if chunk.get("done"):
                break


def stream_response(context: str, history: list[dict], user_message: str) -> Iterator[str]:
    """Stream tokens from Ollama, filtering out any <think> blocks."""
    messages = build_chat_messages(context, history, user_message)
    yield from _filter_think_blocks(_raw_token_stream(messages))


def stream_direct_response(student_profile: dict, user_message: str, intent: str) -> Iterator[str]:
    """Stream a greeting or no-evidence response token by token."""
    student_name = student_profile.get("name", "there")
    student_major = student_profile.get("major", "Computer Science")

    if intent == "greeting":
        prompt = GREETING_PROMPT.format(
            student_name=student_name,
            student_major=student_major,
            user_message=user_message,
        )
    else:
        prompt = NO_EVIDENCE_PROMPT.format(
            student_name=student_name,
            student_major=student_major,
            user_message=user_message,
        )

    try:
        messages = [{"role": "user", "content": prompt}]
        yield from _filter_think_blocks(_raw_token_stream(messages))
    except Exception:
        yield _fallback_direct_response(intent)
