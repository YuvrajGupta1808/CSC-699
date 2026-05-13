import os

OPENROUTER_BASE = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
FIREWORKS_BASE  = os.environ.get("FIREWORKS_BASE_URL",  "https://api.fireworks.ai/inference/v1")

# provider: "openrouter" | "fireworks"
# model_id: the ID to pass to that provider's API
# input_per_m / output_per_m: USD per million tokens
MODELS = {
    # ── OpenRouter models ──────────────────────────────────────────────────
    "llama-3.2-3b": {
        "provider": "openrouter",
        "model_id": "meta-llama/llama-3.2-3b-instruct",
        "input_per_m": 0.015, "output_per_m": 0.025,
    },
    "llama-3.1-8b": {
        "provider": "openrouter",
        "model_id": "meta-llama/llama-3.1-8b-instruct",
        "input_per_m": 0.055, "output_per_m": 0.055,
    },
    "qwen2.5-7b": {
        "provider": "openrouter",
        "model_id": "qwen/qwen-2.5-7b-instruct",
        "input_per_m": 0.050, "output_per_m": 0.150,
    },
    "qwen3-8b": {
        "provider": "openrouter",
        "model_id": "qwen/qwen3-8b",
        "input_per_m": 0.025, "output_per_m": 0.100,
    },
    "mistral-nemo": {
        "provider": "openrouter",
        "model_id": "mistralai/mistral-nemo",
        "input_per_m": 0.035, "output_per_m": 0.080,
    },
    "mistral-small-24b": {
        "provider": "openrouter",
        "model_id": "mistralai/mistral-small-3.2-24b-instruct",
        "input_per_m": 0.065, "output_per_m": 0.065,
    },
    "gemma-3-4b": {
        "provider": "openrouter",
        "model_id": "google/gemma-3-4b-it",
        "input_per_m": 0.030, "output_per_m": 0.030,
    },
    "deepseek-r1": {
        "provider": "openrouter",
        "model_id": "deepseek/deepseek-r1",
        "input_per_m": 0.550, "output_per_m": 2.190,
    },
    "deepseek-v3": {
        "provider": "openrouter",
        "model_id": "deepseek/deepseek-chat-v3-0324",
        "input_per_m": 0.270, "output_per_m": 1.100,
    },
    # ── Fireworks models ───────────────────────────────────────────────────
    "gpt-oss-120b": {
        "provider": "fireworks",
        "model_id": "accounts/fireworks/models/gpt-oss-120b",
        "input_per_m": 0.900, "output_per_m": 0.900,
    },
    "kimi-k2p6": {
        "provider": "fireworks",
        "model_id": "accounts/fireworks/models/kimi-k2p6",
        "input_per_m": 0.140, "output_per_m": 0.140,
    },
}

# Planner and critic held constant across all eval runs
PLANNER_MODEL = "llama-3.2-3b"
CRITIC_MODEL  = "llama-3.2-3b"

# 10 gold questions — two per major category
# GQ-01,03 (job fit), GQ-04,07 (skill gap + course), GQ-12,14 (readiness + comparison),
# GQ-21,22 (strong fit), GQ-26,30 (skill gap w/ jobs + retrieval precision)
EVAL_QUESTION_INDICES = [0, 2, 3, 6, 11, 13, 20, 21, 25, 29]
