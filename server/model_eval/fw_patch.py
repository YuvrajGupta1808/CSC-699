"""
fw_patch.py — Translates Ollama /api/chat calls to OpenRouter or Fireworks.

Usage:
    with model_patch(planner_cfg, generator_cfg, critic_cfg) as tokens:
        result = run_advisor_turn(...)
        print(tokens["input"], tokens["output"])

Each cfg dict must have {"provider": "openrouter"|"fireworks", "model_id": "..."}.
Reverts automatically on context exit. Zero core file changes.
"""

import json
import os
from contextlib import contextmanager
from unittest.mock import patch

import httpx
from openai import OpenAI


def _client(provider: str) -> OpenAI:
    if provider == "fireworks":
        return OpenAI(
            base_url=os.environ["FIREWORKS_BASE_URL"],
            api_key=os.environ["FIREWORKS_API_KEY"],
        )
    return OpenAI(
        base_url=os.environ["OPENROUTER_BASE_URL"],
        api_key=os.environ["OPENROUTER_API_KEY"],
    )


def _call_model(messages: list[dict], cfg: dict) -> tuple[str, dict]:
    """Call OpenRouter or Fireworks and return (content, usage_dict)."""
    resp = _client(cfg["provider"]).chat.completions.create(
        model=cfg["model_id"],
        messages=messages,
        stream=False,
    )
    content = resp.choices[0].message.content or ""
    usage = {
        "prompt_tokens":     resp.usage.prompt_tokens     if resp.usage else 0,
        "completion_tokens": resp.usage.completion_tokens if resp.usage else 0,
    }
    return content, usage


def _fake_ollama_response(content: str, usage: dict) -> httpx.Response:
    body = json.dumps({
        "model": "patched",
        "message": {"role": "assistant", "content": content},
        "done": True,
        "prompt_eval_count": usage["prompt_tokens"],
        "eval_count":        usage["completion_tokens"],
    }).encode()
    return httpx.Response(200, content=body, headers={"content-type": "application/json"})


@contextmanager
def model_patch(planner_cfg: dict, generator_cfg: dict, critic_cfg: dict):
    """
    Context manager that routes Ollama /api/chat calls to the configured model.
    Yields a token counter {"input", "output", "calls"} — reset between questions
    for per-question token counts.

    Routing:
    - critic:    requested model == OLLAMA_CRITIQUE_MODEL env var
    - generator: messages contain a system-role entry
    - planner:   everything else
    """
    critique_model_name = os.environ.get("OLLAMA_CRITIQUE_MODEL", "deepseek-r1:1.5b")
    _original_post = httpx.post
    tokens = {"input": 0, "output": 0, "calls": 0}

    def patched_post(url, *, json=None, **kwargs):
        if json and "/api/chat" in str(url):
            requested = json.get("model", "")
            messages  = json.get("messages", [])

            is_critic  = (requested == critique_model_name)
            has_system = any(m.get("role") == "system" for m in messages)

            cfg = critic_cfg if is_critic else (generator_cfg if has_system else planner_cfg)

            content, usage = _call_model(messages, cfg)
            tokens["input"]  += usage["prompt_tokens"]
            tokens["output"] += usage["completion_tokens"]
            tokens["calls"]  += 1
            return _fake_ollama_response(content, usage)

        return _original_post(url, json=json, **kwargs)

    with patch("httpx.post", patched_post):
        yield tokens


# Convenience alias — kept for backward compatibility
def openrouter_patch(planner_id: str, generator_id: str, critic_id: str):
    from model_eval.config import MODELS
    return model_patch(MODELS[planner_id], MODELS[generator_id], MODELS[critic_id])
