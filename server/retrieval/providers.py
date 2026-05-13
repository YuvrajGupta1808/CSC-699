"""
retrieval/providers.py — Unified LLM + embedding provider abstraction.

Single control surface in .env:

    INFERENCE_PROVIDER = fireworks | openrouter | ollama
    EMBEDDING_PROVIDER = fireworks | openrouter | ollama   (defaults to INFERENCE_PROVIDER)

    CHAT_MODEL     = <model name matching your inference provider>
    PLANNER_MODEL  = <model name matching your inference provider>
    CRITIQUE_MODEL = <model name matching your inference provider>
    EMBED_MODEL    = <model name matching your embedding provider>

Switch providers by changing INFERENCE_PROVIDER and the model names.
See .env.example for ready-to-paste blocks per provider.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Iterator

import httpx

# ---------------------------------------------------------------------------
# Active providers
# ---------------------------------------------------------------------------

PROVIDER       = os.environ.get("INFERENCE_PROVIDER", "ollama").lower()
EMBED_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", PROVIDER).lower()

# ---------------------------------------------------------------------------
# API credentials & base URLs
# ---------------------------------------------------------------------------

_FIREWORKS_KEY  = os.environ.get("FIREWORKS_API_KEY", "")
_FIREWORKS_BASE = os.environ.get("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1")

_OPENROUTER_KEY  = os.environ.get("OPENROUTER_API_KEY", "")
_OPENROUTER_BASE = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

_OLLAMA_BASE = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# ---------------------------------------------------------------------------
# Model name defaults per provider (used when env var is absent)
# ---------------------------------------------------------------------------

_CHAT_DEFAULTS = {
    "fireworks":   "accounts/fireworks/models/llama-v3p3-70b-instruct",
    "openrouter":  "meta-llama/llama-3.3-70b-instruct",
    "ollama":      "llama3.2",
}
_PLANNER_DEFAULTS = {
    "fireworks":   "accounts/fireworks/models/llama-v3p1-8b-instruct",
    "openrouter":  "meta-llama/llama-3.1-8b-instruct",
    "ollama":      "llama3.2",
}
_CRITIQUE_DEFAULTS = {
    "fireworks":   "accounts/fireworks/models/llama-v3p3-70b-instruct",
    "openrouter":  "meta-llama/llama-3.3-70b-instruct",
    "ollama":      "deepseek-r1:1.5b",
}
_EMBED_DEFAULTS = {
    "fireworks":   "nomic-ai/nomic-embed-text-v1.5",
    "openrouter":  "openai/text-embedding-3-small",
    "ollama":      "nomic-embed-text",
}

# Resolve active model names — env var wins, otherwise provider default
_CHAT_MODEL     = os.environ.get("CHAT_MODEL",     _CHAT_DEFAULTS.get(PROVIDER,       "llama3.2"))
_PLANNER_MODEL  = os.environ.get("PLANNER_MODEL",  _PLANNER_DEFAULTS.get(PROVIDER,    "llama3.2"))
_CRITIQUE_MODEL = os.environ.get("CRITIQUE_MODEL", _CRITIQUE_DEFAULTS.get(PROVIDER,   "llama3.2"))
_EMBED_MODEL    = os.environ.get("EMBED_MODEL",    _EMBED_DEFAULTS.get(EMBED_PROVIDER, "nomic-embed-text"))

# ---------------------------------------------------------------------------
# Public accessors
# ---------------------------------------------------------------------------

def chat_model()     -> str: return _CHAT_MODEL
def planner_model()  -> str: return _PLANNER_MODEL
def critique_model() -> str: return _CRITIQUE_MODEL
def embed_model()    -> str: return _EMBED_MODEL


def provider_label() -> str:
    return f"{PROVIDER}/{_CHAT_MODEL.split('/')[-1]}"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _openai_headers(key: str, *, extra: dict | None = None) -> dict:
    h = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if extra:
        h.update(extra)
    return h


def _base_and_headers(provider: str) -> tuple[str, dict]:
    if provider == "fireworks":
        return _FIREWORKS_BASE, _openai_headers(_FIREWORKS_KEY)
    if provider == "openrouter":
        return _OPENROUTER_BASE, _openai_headers(
            _OPENROUTER_KEY,
            extra={"HTTP-Referer": "https://jobskill.local", "X-Title": "JobSkill"},
        )
    return _OLLAMA_BASE, {}


def _strip_think(text: str) -> str:
    """Remove <think>…</think> blocks emitted by reasoning models."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


# ---------------------------------------------------------------------------
# chat_complete — blocking, returns full text
# ---------------------------------------------------------------------------

def chat_complete(
    messages: list[dict],
    *,
    model_role: str = "chat",
    timeout: int = 60,
    temperature: float = 0.2,
) -> str:
    model = {"chat": _CHAT_MODEL, "planner": _PLANNER_MODEL, "critique": _CRITIQUE_MODEL}[model_role]

    if PROVIDER in ("fireworks", "openrouter"):
        base, headers = _base_and_headers(PROVIDER)
        resp = httpx.post(
            f"{base}/chat/completions",
            headers=headers,
            json={"model": model, "messages": messages, "stream": False, "temperature": temperature},
            timeout=timeout,
        )
        resp.raise_for_status()
        return _strip_think(resp.json()["choices"][0]["message"]["content"])

    # Ollama
    resp = httpx.post(
        f"{_OLLAMA_BASE}/api/chat",
        json={"model": model, "messages": messages, "stream": False},
        timeout=timeout,
    )
    resp.raise_for_status()
    return _strip_think(resp.json()["message"]["content"])


# ---------------------------------------------------------------------------
# stream_tokens — yields raw token strings, strips <think> inline
# ---------------------------------------------------------------------------

def stream_tokens(
    messages: list[dict],
    *,
    model_role: str = "chat",
    timeout: int = 120,
    temperature: float = 0.3,
) -> Iterator[str]:
    model = {"chat": _CHAT_MODEL, "planner": _PLANNER_MODEL, "critique": _CRITIQUE_MODEL}[model_role]

    if PROVIDER in ("fireworks", "openrouter"):
        base, headers = _base_and_headers(PROVIDER)
        with httpx.stream(
            "POST",
            f"{base}/chat/completions",
            headers=headers,
            json={"model": model, "messages": messages, "stream": True, "temperature": temperature},
            timeout=timeout,
        ) as response:
            response.raise_for_status()
            buffer = ""
            in_think = False
            for line in response.iter_lines():
                line = line.strip()
                if not line or line == "data: [DONE]":
                    continue
                if line.startswith("data: "):
                    line = line[6:]
                try:
                    token = json.loads(line)["choices"][0].get("delta", {}).get("content") or ""
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
                if not token:
                    continue
                # Inline <think> stripping so reasoning models stream cleanly
                buffer += token
                while True:
                    if in_think:
                        end = buffer.find("</think>")
                        if end >= 0:
                            buffer = buffer[end + 8:]
                            in_think = False
                        else:
                            buffer = ""
                            break
                    else:
                        start = buffer.find("<think>")
                        if start >= 0:
                            if start > 0:
                                yield buffer[:start]
                            buffer = buffer[start + 7:]
                            in_think = True
                        else:
                            safe = max(0, len(buffer) - 7)
                            if safe > 0:
                                yield buffer[:safe]
                                buffer = buffer[safe:]
                            break
            if buffer and not in_think:
                yield buffer
        return

    # Ollama
    with httpx.stream(
        "POST",
        f"{_OLLAMA_BASE}/api/chat",
        json={"model": model, "messages": messages, "stream": True},
        timeout=timeout,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            try:
                chunk = json.loads(line)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield token
                if chunk.get("done"):
                    break
            except json.JSONDecodeError:
                continue


# ---------------------------------------------------------------------------
# embed_text — single text → float vector
# ---------------------------------------------------------------------------

def embed_text(text: str) -> list[float]:
    if EMBED_PROVIDER in ("fireworks", "openrouter"):
        base, headers = _base_and_headers(EMBED_PROVIDER)
        resp = httpx.post(
            f"{base}/embeddings",
            headers=headers,
            json={"model": _EMBED_MODEL, "input": text},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]

    # Ollama
    resp = httpx.post(
        f"{_OLLAMA_BASE}/api/embeddings",
        json={"model": _EMBED_MODEL, "prompt": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]
