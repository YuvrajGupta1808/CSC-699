"""
smoke_test.py — Runs ONE request through Fireworks to verify:
  1. The fw_patch intercepts correctly
  2. Langsmith traces capture Fireworks token counts

Usage:
    cd server && .venv/bin/python3 -m model_eval.smoke_test
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")

from model_eval.config import MODELS, OPENROUTER_BASE, PLANNER_MODEL, CRITIC_MODEL
from model_eval.fw_patch import openrouter_patch as fireworks_patch

PLANNER_FW  = MODELS[PLANNER_MODEL]["or_id"]
CRITIC_FW   = MODELS[CRITIC_MODEL]["or_id"]
GENERATOR_FW = MODELS["qwen2.5-7b"]["or_id"]

print("=" * 60)
print("Smoke Test — Fireworks via fw_patch")
print(f"  Planner  : {PLANNER_MODEL}")
print(f"  Generator: qwen2.5-7b")
print(f"  Critic   : {CRITIC_MODEL}")
print(f"  Base URL : {OPENROUTER_BASE}")
print("=" * 60)

with fireworks_patch(PLANNER_FW, GENERATOR_FW, CRITIC_FW) as tokens:
    from retrieval.graph import run_advisor_turn

    t0 = time.time()
    result = run_advisor_turn(
        user_message="What jobs fit my background?",
        student_id="00000000-0000-0000-0000-000000000001",
        conversation_history=[],
        session_id="smoke-test-fw-001",
    )
    elapsed = round(time.time() - t0, 1)

plan   = result.get("plan", {})
best   = result.get("best_candidate", {})
scores = best.get("scores", {})

input_price  = MODELS["qwen2.5-7b"]["input_per_m"]
output_price = MODELS["qwen2.5-7b"]["output_per_m"]
cost = (tokens["input"] * input_price + tokens["output"] * output_price) / 1_000_000

print(f"\nIntent  : {plan.get('intent')} (classifier={plan.get('classifier')})")
print(f"Reason  : {plan.get('reason')}")
print(f"Scores  : {scores}")
print(f"Time    : {elapsed}s")
print(f"Tokens  : {tokens['input']} input / {tokens['output']} output ({tokens['calls']} LLM calls)")
print(f"Cost    : ${cost:.6f}")
print(f"\nResponse:\n{result.get('final_response', '')[:500]}")
print("\n→ Check Langsmith for token counts and cost on session smoke-test-fw-001")
