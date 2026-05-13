"""
eval_runner.py — Runs 5 representative gold questions with a chosen generator model
on Fireworks and writes a detailed MD report to model_eval/docs/.

Usage:
    cd server && .venv/bin/python3 -m model_eval.eval_runner --model qwen2.5-7b
    cd server && .venv/bin/python3 -m model_eval.eval_runner --model mistral-7b
    cd server && .venv/bin/python3 -m model_eval.eval_runner --model llama-3.2-3b
    cd server && .venv/bin/python3 -m model_eval.eval_runner --model deepseek-r1-8b
"""

import argparse
import sys
import time
import textwrap
from datetime import datetime
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")

from model_eval.config import MODELS, PLANNER_MODEL, CRITIC_MODEL, EVAL_QUESTION_INDICES
from model_eval.fw_patch import model_patch


def compute_cost(input_tokens: int, output_tokens: int, model_key: str) -> float:
    cfg = MODELS[model_key]
    return (input_tokens * cfg["input_per_m"] + output_tokens * cfg["output_per_m"]) / 1_000_000


def run_eval(generator_model_key: str) -> None:
    if generator_model_key not in MODELS:
        print(f"Unknown model '{generator_model_key}'. Choose from: {list(MODELS)}")
        sys.exit(1)

    from tests.gold_questions import GOLD_QUESTIONS
    from retrieval.graph import run_advisor_turn

    planner_cfg   = MODELS[PLANNER_MODEL]
    generator_cfg = MODELS[generator_model_key]
    critic_cfg    = MODELS[CRITIC_MODEL]

    questions = [GOLD_QUESTIONS[i] for i in EVAL_QUESTION_INDICES]

    print(f"\nEvaluating generator: {generator_model_key} ({generator_cfg['provider']})")
    print(f"Planner: {PLANNER_MODEL}  |  Critic: {CRITIC_MODEL}")
    print(f"Questions: {[q['id'] for q in questions]}\n")

    results = []

    with model_patch(planner_cfg, generator_cfg, critic_cfg) as tokens:
        for gq in questions:
            # Reset counter so each question gets its own token tally
            tokens["input"] = tokens["output"] = tokens["calls"] = 0

            print(f"Running {gq['id']} — {gq['student']}...")
            t0 = time.time()
            try:
                result = run_advisor_turn(
                    user_message=gq["message"],
                    student_id=gq["student_id"],
                    conversation_history=[],
                    session_id=f"eval-{generator_model_key}-{gq['id']}-{uuid4().hex[:6]}",
                )
                elapsed = round(time.time() - t0, 1)
                plan   = result.get("plan", {})
                best   = result.get("best_candidate", {})
                scores = best.get("scores", {})
                response_text = result.get("final_response", "")

                input_tok  = tokens["input"]
                output_tok = tokens["output"]
                cost = compute_cost(input_tok, output_tok, generator_model_key)

                results.append({
                    "gq": gq,
                    "status": "ok",
                    "elapsed": elapsed,
                    "intent": plan.get("intent", "?"),
                    "classifier": plan.get("classifier", "?"),
                    "scores": scores,
                    "response": response_text,
                    "input_tok": input_tok,
                    "output_tok": output_tok,
                    "cost": cost,
                    "status_log": result.get("status_log", []),
                })
                print(f"  ✓ {elapsed}s  score={scores.get('total', '?')}/10  tokens={input_tok}in/{output_tok}out  cost=${cost:.6f}")
            except Exception as e:
                elapsed = round(time.time() - t0, 1)
                results.append({
                    "gq": gq,
                    "status": "error",
                    "elapsed": elapsed,
                    "error": str(e),
                    "scores": {},
                    "response": "",
                    "cost": 0.0,
                    "input_tok": 0,
                    "output_tok": 0,
                })
                print(f"  ✗ ERROR: {e}")

    _write_report(generator_model_key, results)


def _write_report(model_key: str, results: list[dict]) -> None:
    docs_dir = Path(__file__).parent / "docs"
    docs_dir.mkdir(exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = docs_dir / f"{model_key}_{ts}.md"

    ok = [r for r in results if r["status"] == "ok"]
    errors = [r for r in results if r["status"] == "error"]
    avg_score   = round(sum(r["scores"].get("total", 0) for r in ok) / max(len(ok), 1), 2)
    avg_elapsed = round(sum(r["elapsed"] for r in ok) / max(len(ok), 1), 1)
    total_cost  = sum(r["cost"] for r in results)
    avg_cost    = round(total_cost / max(len(ok), 1), 6)

    lines = []
    lines.append(f"# Eval Report: {model_key}")
    lines.append(f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    lines.append(f"**Generator:** `{model_key}`  ")
    lines.append(f"**Planner:** `{PLANNER_MODEL}`  **Critic:** `{CRITIC_MODEL}`  ")
    cfg = MODELS[model_key]
    lines.append(f"**Provider:** `{cfg['provider']}`  **Model ID:** `{cfg['model_id']}`")
    lines.append(f"\n**Pricing:** ${cfg['input_per_m']}/M input · ${cfg['output_per_m']}/M output")

    lines.append("\n## Summary\n")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Questions run | {len(results)} |")
    lines.append(f"| Errors | {len(errors)} |")
    lines.append(f"| Avg Score | {avg_score}/10 |")
    lines.append(f"| Avg Latency | {avg_elapsed}s |")
    lines.append(f"| Avg Cost/query | ${avg_cost:.6f} |")
    lines.append(f"| Total Cost | ${total_cost:.6f} |")

    lines.append("\n## Score Overview\n")
    lines.append("| ID | Category | Student | Score | Rel | Sup | Util | Time | Status |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in results:
        gq = r["gq"]
        if r["status"] == "error":
            lines.append(f"| {gq['id']} | {gq['category']} | {gq['student']} | ERROR | — | — | — | {r['elapsed']}s | ❌ |")
        else:
            s = r["scores"]
            lines.append(
                f"| {gq['id']} | {gq['category']} | {gq['student']} | "
                f"**{s.get('total','?')}** | {s.get('relevance','?')} | {s.get('support','?')} | "
                f"{s.get('utility','?')} | {r['elapsed']}s | ✅ |"
            )

    lines.append("\n## Per-Question Results\n")
    for r in results:
        gq = r["gq"]
        lines.append(f"### {gq['id']} — {gq['category']} ({gq['student']})")
        lines.append(f"\n**Question:** {gq['message']}")
        lines.append(f"\n**Eval criteria:** _{gq['eval_criteria']}_\n")

        if r["status"] == "error":
            lines.append(f"**ERROR:** {r['error']}\n")
            lines.append("---\n")
            continue

        s = r["scores"]
        lines.append(
            f"**Score:** {s.get('total','?')}/10 "
            f"(rel={s.get('relevance','?')}, sup={s.get('support','?')}, util={s.get('utility','?')})  "
        )
        lines.append(f"**Intent:** `{r['intent']}` ({r['classifier']})  ")
        lines.append(f"**Time:** {r['elapsed']}s")
        if r["input_tok"] or r["output_tok"]:
            lines.append(f"**Tokens:** {r['input_tok']} in / {r['output_tok']} out  **Cost:** ${r['cost']:.6f}")

        critique = s.get("critique", "")
        if critique:
            lines.append(f"\n**Critic note:** _{critique}_")

        lines.append(f"\n**Pipeline:** {' → '.join(r['status_log'])}")

        lines.append("\n**Response:**\n")
        wrapped = textwrap.fill(r["response"], width=100)
        for line in wrapped.splitlines():
            lines.append(f"> {line}")

        lines.append("\n---\n")

    report = "\n".join(lines)
    out_path.write_text(report)
    print(f"\nReport written → {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run model eval against Fireworks")
    parser.add_argument("--model", required=True, choices=list(MODELS), help="Generator model to evaluate")
    args = parser.parse_args()
    run_eval(args.model)
