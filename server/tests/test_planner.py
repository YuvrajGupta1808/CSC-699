import unittest
from unittest.mock import patch

from retrieval.planner import plan_retrieval


def _no_llm(question, history_summary):
    """Force keyword fallback by making the LLM classifier always return None."""
    return None


class PlannerRegressionTests(unittest.TestCase):
    """Keyword-fallback regression tests — LLM classifier is patched out."""

    def _plan(self, question, history=None):
        with patch("retrieval.planner._llm_classify_intent", side_effect=_no_llm):
            return plan_retrieval(question, history)

    def test_explain_does_not_trigger_broad_plan_keyword(self):
        result = self._plan("Explain backend roles for new grads")
        self.assertEqual(result["intent"], "jobs")
        self.assertEqual(result["top_k_jobs"], 6)
        self.assertEqual(result["top_k_courses"], 2)

    def test_career_path_phrase_still_triggers_broad_analysis(self):
        result = self._plan("What career path should I follow for ML engineering?")
        self.assertEqual(result["intent"], "broad")
        self.assertEqual(result["top_k_jobs"], 6)
        self.assertEqual(result["top_k_courses"], 6)

    def test_course_questions_retrieve_enough_courses(self):
        result = self._plan("What courses should I take to learn machine learning?")
        self.assertIn(result["intent"], ("courses", "skill_gap"))
        self.assertGreaterEqual(result["top_k_courses"], 4)

    def test_skill_gap_always_retrieves_jobs(self):
        result = self._plan("What courses should I take to close my ML skill gaps?")
        self.assertEqual(result["intent"], "skill_gap")
        self.assertGreaterEqual(result["top_k_jobs"], 2)
        self.assertGreaterEqual(result["top_k_courses"], 4)

    def test_llm_classifier_falls_back_on_none(self):
        # When LLM returns None, keyword fallback should produce a valid dict
        with patch("retrieval.planner._llm_classify_intent", return_value=None):
            result = plan_retrieval("What jobs fit my background?")
        self.assertIn("intent", result)
        self.assertEqual(result.get("classifier"), "keyword_fallback")

    def test_followup_with_history_uses_context(self):
        history = [{"role": "user", "content": "show me backend jobs"}]
        result = self._plan("what about those?", history=history)
        self.assertGreaterEqual(result["top_k_jobs"], 1)


if __name__ == "__main__":
    unittest.main()
