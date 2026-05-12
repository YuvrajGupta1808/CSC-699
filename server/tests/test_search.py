import unittest
from unittest.mock import MagicMock

from retrieval.text_utils import query_terms
from retrieval.search import _max_pool_by_record, _rrf_rerank


def _weaviate_obj(props: dict, score: float):
    obj = MagicMock()
    obj.properties = props
    obj.metadata.score = score
    return obj


class SearchHelperTests(unittest.TestCase):
    def test_query_terms_extract_user_intent_tokens(self):
        terms = query_terms("Backend roles for ML grads")
        self.assertIn("backend", terms)
        self.assertIn("roles", terms)
        self.assertIn("grads", terms)

    def test_query_terms_ignore_short_tokens(self):
        terms = query_terms("Go AI ML")
        self.assertEqual(terms, set())

    def test_query_terms_normalizes_aliases(self):
        # "node.js" (6 chars) normalizes to "nodejs"; both kept in result set
        terms = query_terms("node.js backend")
        self.assertIn("nodejs", terms)
        self.assertIn("backend", terms)


class MaxPoolTests(unittest.TestCase):
    def test_max_pool_keeps_best_score_per_record(self):
        objs = [
            _weaviate_obj({"job_id": "j1", "title": "Eng", "skills": []}, 0.8),
            _weaviate_obj({"job_id": "j1", "title": "Eng", "skills": []}, 0.5),
            _weaviate_obj({"job_id": "j2", "title": "PM",  "skills": []}, 0.7),
        ]
        pooled = _max_pool_by_record(objs, "job_id")
        self.assertEqual(len(pooled), 2)
        j1 = next(p for p in pooled if p["job_id"] == "j1")
        self.assertAlmostEqual(j1["_raw_score"], 0.8)

    def test_max_pool_skips_missing_id(self):
        objs = [
            _weaviate_obj({"title": "No ID"}, 0.9),
            _weaviate_obj({"job_id": "j1", "title": "Has ID"}, 0.5),
        ]
        pooled = _max_pool_by_record(objs, "job_id")
        self.assertEqual(len(pooled), 1)
        self.assertEqual(pooled[0]["job_id"], "j1")

    def test_max_pool_preserves_all_properties(self):
        objs = [_weaviate_obj({"job_id": "j1", "title": "T", "company": "C", "skills": ["Python"]}, 0.6)]
        pooled = _max_pool_by_record(objs, "job_id")
        self.assertEqual(pooled[0]["title"], "T")
        self.assertEqual(pooled[0]["company"], "C")
        self.assertEqual(pooled[0]["skills"], ["Python"])


class RRFRerankTests(unittest.TestCase):
    def test_rrf_produces_expected_ordering(self):
        hits = [
            {"job_id": "a", "semantic_score": 0.9, "skill_overlap": 1},
            {"job_id": "b", "semantic_score": 0.5, "skill_overlap": 5},
            {"job_id": "c", "semantic_score": 0.7, "skill_overlap": 0},
        ]
        reranked = _rrf_rerank(hits, ["semantic_score", "skill_overlap"])
        ids = [h["job_id"] for h in reranked]
        # "a" wins semantic, "b" wins overlap — RRF blends both
        self.assertEqual(len(ids), 3)
        self.assertIn("rrf_score", reranked[0])

    def test_rrf_removes_temp_rank_fields(self):
        hits = [{"x": 0.8}, {"x": 0.5}]
        reranked = _rrf_rerank(hits, ["x"])
        for h in reranked:
            self.assertNotIn("_rank_x", h)


if __name__ == "__main__":
    unittest.main()
