import os
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from langsmith import trace

from retrieval.graph import _critique_candidate_branch, _generate_candidate_branch, run_advisor_turn
from retrieval.observability import (
    langsmith_dataset_name,
    ollama_timing_metadata,
    ollama_usage_metadata,
)


class ObservabilityTests(unittest.TestCase):
    def test_ollama_usage_metadata_includes_tokens_and_costs(self):
        payload = {
            "prompt_eval_count": 120,
            "eval_count": 30,
        }
        with patch.dict(
            os.environ,
            {
                "OLLAMA_INPUT_TOKEN_COST_USD": "0.000001",
                "OLLAMA_OUTPUT_TOKEN_COST_USD": "0.000002",
            },
            clear=False,
        ):
            usage = ollama_usage_metadata(payload)

        self.assertEqual(usage["input_tokens"], 120)
        self.assertEqual(usage["output_tokens"], 30)
        self.assertEqual(usage["total_tokens"], 150)
        self.assertAlmostEqual(usage["input_cost"], 0.00012)
        self.assertAlmostEqual(usage["output_cost"], 0.00006)
        self.assertAlmostEqual(usage["total_cost"], 0.00018)

    def test_ollama_timing_metadata_converts_nanoseconds_to_seconds(self):
        payload = {
            "load_duration": 500_000_000,
            "prompt_eval_duration": 1_500_000_000,
            "eval_duration": 2_250_000_000,
            "total_duration": 4_250_000_000,
        }
        timing = ollama_timing_metadata(payload)

        self.assertEqual(timing["load_seconds"], 0.5)
        self.assertEqual(timing["prompt_eval_seconds"], 1.5)
        self.assertEqual(timing["completion_seconds"], 2.25)
        self.assertEqual(timing["total_seconds"], 4.25)

    def test_langsmith_dataset_name_defaults_to_project_suffix(self):
        with patch.dict(
            os.environ,
            {
                "LANGSMITH_DATASET": "",
                "LANGSMITH_PROJECT": "jobskill",
            },
            clear=False,
        ):
            self.assertEqual(langsmith_dataset_name(), "jobskill-reference-examples")

    def test_generate_candidate_branch_updates_visible_llm_run(self):
        state = {
            "turn_id": "turn-1",
            "session_id": "session-1",
            "student_id": "student-1",
            "user_message": "What jobs fit me?",
            "selected_job_id": None,
        }
        view = {
            "label": "Top Match",
            "evidence_description": "Best candidate",
            "context": "Evidence context",
        }
        details = {
            "text": "Grounded answer",
            "usage_metadata": {"input_tokens": 120, "output_tokens": 30, "total_tokens": 150},
            "timing_metadata": {"total_seconds": 1.2},
            "metadata": {"provider": "ollama"},
            "outputs": {"response": "Grounded answer"},
            "first_token_time": datetime(2026, 5, 10, tzinfo=timezone.utc),
        }

        with trace("parent", run_type="chain") as parent_run:
            with patch("retrieval.graph.generate_candidate_details", return_value=details), patch(
                "retrieval.graph.persist_run_tree"
            ) as persist_run_tree:
                result = _generate_candidate_branch(
                    parent_run=parent_run,
                    state=state,
                    view=view,
                    conversation_snapshot=[],
                )

        self.assertEqual(result["text"], "Grounded answer")
        self.assertEqual(result["_trace_metrics"][0]["usage_metadata"]["total_tokens"], 150)
        run = persist_run_tree.call_args.args[0]
        self.assertEqual(run.run_type, "llm")
        self.assertEqual(persist_run_tree.call_args.kwargs["usage_metadata"]["total_tokens"], 150)

    def test_critique_candidate_branch_updates_visible_llm_run(self):
        state = {
            "turn_id": "turn-1",
            "session_id": "session-1",
            "student_id": "student-1",
            "user_message": "What skills am I missing?",
            "selected_job_id": None,
            "bundle": {"jobs": [], "courses": []},
        }
        candidate = {
            "view": {
                "label": "Top Match",
                "evidence_description": "Best candidate",
                "context": "Evidence context",
            },
            "text": "Grounded answer",
        }
        critique_details = {
            "scores": {"relevance": 8, "support": 9, "utility": 7, "critique": "", "support_findings": [], "total": 8.2},
            "usage_metadata": {"input_tokens": 90, "output_tokens": 20, "total_tokens": 110},
            "timing_metadata": {"total_seconds": 0.8},
            "raw_response": "{\"relevance\":8}",
        }

        with trace("parent", run_type="chain") as parent_run:
            with patch("retrieval.graph.critique_candidate_details", return_value=critique_details), patch(
                "retrieval.graph.persist_run_tree"
            ) as persist_run_tree:
                result = _critique_candidate_branch(
                    parent_run=parent_run,
                    state=state,
                    candidate=candidate,
                )

        self.assertEqual(result["scores"]["total"], 8.2)
        run = persist_run_tree.call_args.args[0]
        self.assertEqual(run.run_type, "llm")
        self.assertEqual(persist_run_tree.call_args.kwargs["usage_metadata"]["total_tokens"], 110)

    def test_run_advisor_turn_aggregates_llm_usage_to_root_run(self):
        result = {
            "plan": {"intent": "jobs"},
            "bundle": {"jobs": [], "courses": []},
            "candidate_views": [],
            "candidates": [
                {
                    "view": {"label": "A"},
                    "text": "A",
                    "scores": {"total": 8.0},
                    "_trace_metrics": [
                        {
                            "usage_metadata": {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120},
                            "first_token_time": datetime(2026, 5, 10, 12, 0, tzinfo=timezone.utc),
                        },
                        {
                            "usage_metadata": {"input_tokens": 80, "output_tokens": 10, "total_tokens": 90},
                            "first_token_time": None,
                        },
                    ],
                }
            ],
            "best_candidate": {"view": {"label": "A"}},
            "runner_up": None,
            "score_gap": 8.0,
            "final_response": "A",
            "status_log": [],
        }

        with patch("retrieval.graph.ADVISOR_GRAPH.invoke", return_value=result), patch(
            "retrieval.graph.persist_run_tree"
        ) as persist_run_tree, patch(
            "retrieval.graph.automate_feedback", return_value=[]
        ), patch(
            "retrieval.graph.automate_reference_example", return_value=None
        ):
            run_advisor_turn(
                user_message="What jobs fit me?",
                student_id="student-1",
                conversation_history=[],
                session_id="session-1",
            )

        root_run = persist_run_tree.call_args.args[0]
        self.assertEqual(root_run.name, "advisor_turn")
        self.assertEqual(persist_run_tree.call_args.kwargs["usage_metadata"]["total_tokens"], 210)


if __name__ == "__main__":
    unittest.main()
