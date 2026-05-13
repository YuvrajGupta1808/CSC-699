"""
model_comparison.py — Compare multiple local Ollama models on the career advisor
                       system, scored by RAGAS (OpenAI gpt-4o-mini as judge).

What this measures
──────────────────
  Faithfulness        does the model stick to retrieved evidence? (no hallucinations)
  Response Relevancy  does the model actually answer the question asked?
  Context Precision   do the top retrieved chunks support the response?
                      (slight variance per model — mostly reflects retrieval quality)
  Internal Total      deepseek-r1 critique score kept as a secondary reference

The advisor pipeline (retrieval, embedding, critique) stays 100% local.
OpenAI is used only as the RAGAS judge — it never generates advisor responses.

Usage
─────
  # Pull the models you want to test first:
  ollama pull mistral
  ollama pull qwen2.5:7b
  ollama pull llama3.1:8b
  # llama3.2 + deepseek-r1:1.5b are already pulled

  # Run comparison — 10 representative questions × 4 models (~$0.02, ~20 min):
  PYTHONPATH=server python ragas/model_comparison.py

  # All 30 gold questions:
  PYTHONPATH=server python ragas/model_comparison.py --all

  # Specific models only:
  PYTHONPATH=server python ragas/model_comparison.py --models llama3.2 mistral

  # Resume an interrupted run:
  PYTHONPATH=server python ragas/model_comparison.py --resume

Output
──────
  ragas/comparison_results.json   raw scores for all models × questions
  ragas/comparison_report.md      human-readable summary + per-question breakdown
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

# ── Path setup ─────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent   # CSC-699/
sys.path.insert(0, str(REPO_ROOT / "server"))        # retrieval.*, tests.*, eval.*
sys.path.insert(0, str(REPO_ROOT / "ragas"))         # evaluator module

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")

import retrieval.llm as _llm_module
import retrieval.planner as _planner_module
from retrieval.graph import run_advisor_turn
from evaluator import actual_context_to_chunks, bundle_to_contexts, evaluate_samples, ragas_avg
from tests.gold_questions import GOLD_QUESTIONS

# ── Config ─────────────────────────────────────────────────────────────────────

DEFAULT_MODELS = [
    "llama3.2",       # 3.2B  baseline (already pulled)
    "mistral",        # 7B    strong general-purpose
    "qwen2.5:7b",     # 7B    strong reasoning + instruction following
    "llama3.1:8b",    # 8B    Meta's latest 8B
]

# 10 questions covering every category — run fast and cheaply by default
REPRESENTATIVE_IDS = [
    "GQ-01",   # Specific Job Fit
    "GQ-04",   # Skill Gap Analysis
    "GQ-06",   # Skill Gap — prioritization
    "GQ-07",   # Course Recommendation
    "GQ-10",   # Career Readiness
    "GQ-13",   # Job Comparison
    "GQ-15",   # Action Plan
    "GQ-17",   # Domain Pivot
    "GQ-22",   # Strong Fit — cloud/DevOps
    "GQ-25",   # Cross-Disciplinary
]

RESULTS_PATH = Path(__file__).parent / "comparison_results.json"
REPORT_PATH  = Path(__file__).parent / "comparison_report.md"


# ── Model switching ────────────────────────────────────────────────────────────

def _set_model(model: str) -> None:
    """Patch the module-level CHAT_MODEL so the next advisor turn uses this model."""
    _llm_module.CHAT_MODEL = model
    _planner_module.CHAT_MODEL = model


# ── Single question run ────────────────────────────────────────────────────────

def run_question(gq: dict, model: str) -> dict:
    _set_model(model)
    print(f"    [{gq['id']}] {gq['message'][:65]}...")
    t0 = time.time()
    try:
        result = run_advisor_turn(
            user_message=gq["message"],
            student_id=gq["student_id"],
            conversation_history=[],
            session_id=f"compare-{model}-{gq['id']}-{uuid4()}",
        )
        elapsed = round(time.time() - t0, 1)
        best   = result.get("best_candidate", {})
        scores = best.get("scores", {})
        bundle = result.get("bundle", {})

        # Use the ACTUAL context the model saw — not a reconstructed summary.
        # This is what the model used to generate the response, so RAGAS
        # faithfulness correctly checks claims against the same evidence.
        actual_ctx = best.get("view", {}).get("context", "")
        contexts = actual_context_to_chunks(actual_ctx) if actual_ctx else bundle_to_contexts(bundle)

        return {
            "id":       gq["id"],
            "category": gq["category"],
            "student":  gq["student"],
            "message":  gq["message"],
            "model":    model,
            "status":   "ok",
            "elapsed_s": elapsed,
            "response":  result.get("final_response", ""),
            "contexts":  contexts,
            "plan":      result.get("plan", {}),
            "internal_scores": {
                "relevance": scores.get("relevance"),
                "support":   scores.get("support"),
                "utility":   scores.get("utility"),
                "total":     scores.get("total"),
            },
            "ragas_scores": None,
            "ragas_avg":    None,
        }
    except Exception as exc:
        elapsed = round(time.time() - t0, 1)
        print(f"      ERROR: {exc}")
        return {
            "id": gq["id"], "category": gq["category"], "student": gq["student"],
            "message": gq["message"], "model": model, "status": "error",
            "elapsed_s": elapsed, "error": str(exc),
            "response": "", "contexts": [], "plan": {},
            "internal_scores": {}, "ragas_scores": None, "ragas_avg": None,
        }


# ── RAGAS batch ────────────────────────────────────────────────────────────────

def run_ragas_batch(runs: list[dict]) -> list[dict]:
    ok = [r for r in runs if r["status"] == "ok" and r["contexts"]]
    if not ok:
        return runs
    print(f"\n  Scoring {len(ok)} sample(s) with RAGAS (OpenAI gpt-4o-mini judge)...")
    samples = [{"user_input": r["message"], "response": r["response"], "retrieved_contexts": r["contexts"]} for r in ok]
    try:
        scores_list = evaluate_samples(samples)
        for run, scores in zip(ok, scores_list):
            run["ragas_scores"] = scores
            run["ragas_avg"] = ragas_avg(scores)
        print("  RAGAS scoring complete.")
    except Exception as exc:
        print(f"  RAGAS scoring failed: {exc}")
        for run in ok:
            run["ragas_scores"] = {}
            run["ragas_avg"] = None
    return runs


# ── Report generation ──────────────────────────────────────────────────────────

def _f(v, d=2):
    return "—" if v is None else f"{v:.{d}f}"

def _em(v):
    if v is None: return ""
    return "🟢" if v >= 0.8 else ("🟡" if v >= 0.6 else "🔴")

def _model_avg(all_runs, model, key, sub=None):
    vals = []
    for r in all_runs:
        if r["model"] != model or r["status"] != "ok": continue
        src = r.get("ragas_scores" if sub is None else sub) or {}
        v = src.get(key)
        if v is not None: vals.append(v)
    return round(sum(vals)/len(vals), 3) if vals else None


def generate_report(all_runs: list[dict], models: list[str], run_at: str) -> str:
    lines = [
        "# Model Comparison Report",
        f"\n**Run date:** {run_at}",
        f"**RAGAS judge:** OpenAI gpt-4o-mini  ",
        f"**Advisor pipeline:** 100% local (Ollama + Weaviate)  ",
        f"**Models compared:** {', '.join(f'`{m}`' for m in models)}",
        f"**Questions:** {len(set(r['id'] for r in all_runs))}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Model | Faithfulness ↑ | Resp. Relevancy ↑ | Ctx Precision | RAGAS Avg ↑ | Internal /10 | Avg Time |",
        "|---|---|---|---|---|---|---|",
    ]

    for m in models:
        faith = _model_avg(all_runs, m, "faithfulness")
        rel   = _model_avg(all_runs, m, "response_relevancy")
        ctx   = _model_avg(all_runs, m, "context_precision")
        ravg  = _model_avg(all_runs, m, "ragas_avg")
        itot  = _model_avg(all_runs, m, "total", sub="internal_scores")
        ok_r  = [r for r in all_runs if r["model"] == m and r["status"] == "ok"]
        avgt  = round(sum(r["elapsed_s"] for r in ok_r)/len(ok_r), 1) if ok_r else None
        lines.append(
            f"| `{m}` "
            f"| {_em(faith)}{_f(faith)} "
            f"| {_em(rel)}{_f(rel)} "
            f"| {_f(ctx)} "
            f"| **{_f(ravg)}** "
            f"| {_f(itot, 1)} "
            f"| {_f(avgt, 1)}s |"
        )

    lines += [
        "",
        "> **Faithfulness** and **Response Relevancy** are the primary model comparison metrics.  ",
        "> **Context Precision** reflects retrieval quality — slight variance per model is expected.",
        "",
        "---",
        "",
        "## Per-Question Breakdown",
        "",
    ]

    for qid in dict.fromkeys(r["id"] for r in all_runs):
        q_runs = [r for r in all_runs if r["id"] == qid]
        ref = q_runs[0]
        lines += [
            f"### {qid} — {ref['category']} ({ref['student']})",
            f"**Query:** _{ref['message']}_",
            "",
            "| Model | Faith | Rel | CtxP | RAGAS | Internal | Time |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in q_runs:
            if r["status"] == "error":
                lines.append(f"| `{r['model']}` | — | — | — | — | — | {r['elapsed_s']}s |")
                continue
            rs = r.get("ragas_scores") or {}
            fi, rv, cp = rs.get("faithfulness"), rs.get("response_relevancy"), rs.get("context_precision")
            lines.append(
                f"| `{r['model']}` "
                f"| {_em(fi)}{_f(fi)} "
                f"| {_em(rv)}{_f(rv)} "
                f"| {_f(cp)} "
                f"| **{_f(r.get('ragas_avg'))}** "
                f"| {_f((r.get('internal_scores') or {}).get('total'), 1)} "
                f"| {r['elapsed_s']}s |"
            )
        lines.append("")

        for r in q_runs:
            if r["status"] == "ok":
                lines += [
                    f"<details><summary><code>{r['model']}</code></summary>",
                    "",
                    f"> {r['response'][:900].replace(chr(10), chr(10) + '> ')}",
                    "",
                    "</details>",
                    "",
                ]
        lines += ["---", ""]

    # Key findings
    lines += ["## Key Findings", ""]
    model_avgs = sorted(
        [(m, _model_avg(all_runs, m, "ragas_avg")) for m in models if _model_avg(all_runs, m, "ragas_avg") is not None],
        key=lambda x: -(x[1] or 0),
    )
    if model_avgs:
        best, bv = model_avgs[0]
        worst, wv = model_avgs[-1]
        lines.append(f"- **Best RAGAS average:** `{best}` ({bv:.3f})")
        lines.append(f"- **Lowest RAGAS average:** `{worst}` ({wv:.3f})")
        if len(model_avgs) > 1:
            lines.append(f"- **Gap:** {bv - wv:.3f}")
    ok_runs = [r for r in all_runs if r["status"] == "ok"]
    if ok_runs:
        fastest = min(models, key=lambda m: sum(r["elapsed_s"] for r in ok_runs if r["model"] == m) / max(sum(1 for r in ok_runs if r["model"] == m), 1))
        slowest = max(models, key=lambda m: sum(r["elapsed_s"] for r in ok_runs if r["model"] == m) / max(sum(1 for r in ok_runs if r["model"] == m), 1))
        lines.append(f"- **Fastest model:** `{fastest}`")
        lines.append(f"- **Slowest model:** `{slowest}`")
    lines.append("")
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Compare local Ollama models with RAGAS")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--limit", type=int, default=None, help="Limit to first N questions")
    parser.add_argument("--all",   action="store_true",   help="Run all 30 gold questions")
    parser.add_argument("--resume",action="store_true",   help="Load existing results and skip completed runs")
    args = parser.parse_args()

    if args.all:
        questions = GOLD_QUESTIONS
    else:
        by_id = {q["id"]: q for q in GOLD_QUESTIONS}
        questions = [by_id[i] for i in REPRESENTATIVE_IDS if i in by_id]
    if args.limit:
        questions = questions[:args.limit]

    models = args.models

    print("=" * 68)
    print("  Career Advisor — Model Comparison")
    print("=" * 68)
    print(f"  Models   : {', '.join(models)}")
    print(f"  Questions: {len(questions)}")
    print(f"  Judge    : OpenAI gpt-4o-mini (RAGAS only)")
    print("=" * 68)

    all_runs: list[dict] = []
    completed: set[tuple] = set()
    if args.resume and RESULTS_PATH.exists():
        all_runs = json.loads(RESULTS_PATH.read_text())
        completed = {(r["model"], r["id"]) for r in all_runs}
        print(f"\nResuming — {len(completed)} runs already done.")

    for model in models:
        needed = [q for q in questions if (model, q["id"]) not in completed]
        if not needed:
            print(f"\n  {model}: all complete, skipping.")
            continue
        print(f"\n  Model: {model}  ({len(needed)} question(s))")
        new_runs: list[dict] = []
        for gq in needed:
            run = run_question(gq, model)
            new_runs.append(run)
            all_runs.append(run)
            completed.add((model, gq["id"]))
            RESULTS_PATH.write_text(json.dumps(all_runs, indent=2, default=str))

        new_runs = run_ragas_batch(new_runs)
        idx = {(r["model"], r["id"]): i for i, r in enumerate(all_runs)}
        for r in new_runs:
            k = (r["model"], r["id"])
            if k in idx:
                all_runs[idx[k]] = r
        RESULTS_PATH.write_text(json.dumps(all_runs, indent=2, default=str))

    run_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    REPORT_PATH.write_text(generate_report(all_runs, models, run_at), encoding="utf-8")

    print("\n" + "=" * 68)
    print("  RESULTS")
    print("=" * 68)
    for m in models:
        ok_r = [r for r in all_runs if r["model"] == m and r["status"] == "ok"]
        if not ok_r: continue
        rvs = [r["ragas_avg"] for r in ok_r if r.get("ragas_avg") is not None]
        ivs = [(r.get("internal_scores") or {}).get("total") for r in ok_r]
        ivs = [v for v in ivs if v is not None]
        ravg = round(sum(rvs)/len(rvs), 3) if rvs else None
        iavg = round(sum(ivs)/len(ivs), 2) if ivs else None
        avgt = round(sum(r["elapsed_s"] for r in ok_r)/len(ok_r), 1)
        print(f"  {m:<22} RAGAS {_f(ravg)}  Internal {_f(iavg,1)}/10  {avgt}s avg")

    print(f"\n  Report : {REPORT_PATH}")
    print(f"  Raw    : {RESULTS_PATH}")


if __name__ == "__main__":
    main()
