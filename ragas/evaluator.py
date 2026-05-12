"""
evaluator.py — RAGAS evaluation wrapper for the career advisor system.

Uses OpenAI (gpt-4o-mini) as the RAGAS judge LLM for reliable structured output.
Local nomic-embed-text handles embedding-based metrics.

Metrics (all reference-free — no ground truth answers required):
  Faithfulness                        are all claims grounded in retrieved context?
  ResponseRelevancy                   does the response actually answer the question?
  LLMContextPrecisionWithoutReference are the retrieved chunks relevant to the query?

Run:
  PYTHONPATH=server python ragas/model_comparison.py
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# ── Judge LLM: OpenAI via RAGAS ────────────────────────────────────────────────

def _build_judge_llm():
    from openai import OpenAI
    from ragas.llms import llm_factory
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set in .env — add it to use RAGAS evaluation."
        )
    return llm_factory("gpt-4o-mini", provider="openai", client=OpenAI(api_key=api_key))


def _build_judge_embeddings():
    from langchain_ollama import OllamaEmbeddings
    from ragas.embeddings import LangchainEmbeddingsWrapper
    return LangchainEmbeddingsWrapper(OllamaEmbeddings(
        model=os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
        base_url=os.environ.get("OLLAMA_URL", "http://localhost:11434"),
    ))


# ── Core evaluation function ───────────────────────────────────────────────────

def evaluate_samples(samples: list[dict[str, Any]]) -> list[dict[str, float | None]]:
    """
    Evaluate a list of advisor turn samples with RAGAS.

    Each sample dict must contain:
        user_input         str        the student's question
        response           str        the advisor's final response
        retrieved_contexts list[str]  text excerpts from the evidence bundle

    Returns a parallel list of score dicts:
        faithfulness, response_relevancy, context_precision  — each 0.0–1.0 or None
    """
    from ragas.dataset_schema import SingleTurnSample, EvaluationDataset
    from ragas.metrics import Faithfulness, ResponseRelevancy
    from ragas.metrics import LLMContextPrecisionWithoutReference
    from ragas.run_config import RunConfig
    from ragas import evaluate

    judge_llm = _build_judge_llm()
    judge_emb = _build_judge_embeddings()

    dataset = EvaluationDataset(samples=[
        SingleTurnSample(
            user_input=s["user_input"],
            response=s["response"],
            retrieved_contexts=s["retrieved_contexts"],
        )
        for s in samples
    ])

    results = evaluate(
        dataset=dataset,
        metrics=[
            Faithfulness(llm=judge_llm),
            ResponseRelevancy(llm=judge_llm, embeddings=judge_emb),
            LLMContextPrecisionWithoutReference(llm=judge_llm),
        ],
        run_config=RunConfig(timeout=120, max_retries=5, max_workers=3),
        raise_exceptions=False,
    )

    df = results.to_pandas()
    return [
        {
            "faithfulness":       _safe(row.get("faithfulness")),
            "response_relevancy": _safe(row.get("answer_relevancy")),
            "context_precision":  _safe(row.get("llm_context_precision_without_reference")),
        }
        for _, row in df.iterrows()
    ]


def _safe(value) -> float | None:
    try:
        v = float(value)
        return round(v, 3) if v == v else None  # NaN guard
    except (TypeError, ValueError):
        return None


def ragas_avg(scores: dict[str, float | None]) -> float | None:
    vals = [v for v in scores.values() if v is not None]
    return round(sum(vals) / len(vals), 3) if vals else None


# ── Context extraction ─────────────────────────────────────────────────────────

def actual_context_to_chunks(context: str) -> list[str]:
    """
    Split the full context string the model actually used into logical sections
    for RAGAS evaluation.  This is the correct way to build retrieved_contexts:
    pass exactly what the model saw, not a reconstructed summary.

    The context string is structured with headers like:
      STUDENT PROFILE
      RELEVANT JOB POSTINGS (...)
      RELEVANT COURSES (...)
    Split on double-newline paragraph breaks and return non-empty sections.
    """
    # Split by double-newline (paragraph breaks between sections)
    sections = [s.strip() for s in context.split("\n\n") if s.strip()]
    # Keep sections that contain meaningful content (> 20 chars)
    return [s for s in sections if len(s) > 20]


def bundle_to_contexts(bundle: dict) -> list[str]:
    """
    Fallback: build context strings from the bundle dict when the actual
    model context string is not available.  Less accurate for RAGAS than
    actual_context_to_chunks() because it lacks the student profile and
    the structured Gaps/Covers lines the model used.
    """
    contexts: list[str] = []
    for job in bundle.get("jobs", []):
        parts = [f"Job: {job.get('title', '')} at {job.get('company', '')}"]
        if job.get("required_skills"):
            parts.append(f"Required skills: {', '.join(job['required_skills'])}")
        if job.get("covered"):
            parts.append(f"Student covers: {', '.join(job['covered'])}")
        if job.get("gaps"):
            parts.append(f"Gaps: {', '.join(job['gaps'])}")
        if job.get("description_excerpt"):
            parts.append(job["description_excerpt"])
        contexts.append("\n".join(p for p in parts if p))
    for course in bundle.get("courses", []):
        parts = [f"Course: {course.get('course_code', '')} {course.get('title', '')}"]
        if course.get("teaches"):
            parts.append(f"Teaches: {', '.join(course['teaches'])}")
        if course.get("description_excerpt"):
            parts.append(course["description_excerpt"])
        contexts.append("\n".join(p for p in parts if p))
    return [c for c in contexts if c.strip()]
