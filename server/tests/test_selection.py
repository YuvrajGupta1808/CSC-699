import unittest


class SelectionLogicTests(unittest.TestCase):
    def test_highest_score_candidate_remains_selected(self):
        candidates = [
            {
                "view": {"label": "A — Specific Job"},
                "scores": {"total": 8.9},
            },
            {
                "view": {"label": "C — Course Path"},
                "scores": {"total": 9.0},
            },
        ]
        ranked = sorted(candidates, key=lambda candidate: candidate["scores"]["total"], reverse=True)
        best_candidate = ranked[0]
        runner_up = ranked[1]
        score_gap = max(0.0, best_candidate["scores"]["total"] - runner_up["scores"]["total"])
        self.assertEqual(best_candidate["view"]["label"], "C — Course Path")
        self.assertAlmostEqual(score_gap, 0.1, places=6)


if __name__ == "__main__":
    unittest.main()
