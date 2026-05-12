import unittest

from retrieval.critique import _allowed_entities, _validate_citations, critique_candidate


class CitationValidationTests(unittest.TestCase):
    """Unit tests for the structured citation validator (_validate_citations)."""

    def _entities(self, bundle):
        return _allowed_entities(bundle)

    def test_citation_pointing_to_real_job_title_is_allowed(self):
        bundle = {
            "student": {"skills": ["Python"], "completed_courses": []},
            "jobs": [{"title": "Backend Engineer", "company": "Acme", "required_skills": ["Python"], "covered": ["Python"], "gaps": []}],
            "courses": [],
        }
        entities = self._entities(bundle)
        citations = [{"claim": "fits your background", "source": "backend engineer"}]
        violations = _validate_citations(citations, entities)
        self.assertEqual(violations, [])

    def test_citation_pointing_to_hallucinated_job_title_is_flagged(self):
        bundle = {
            "student": {"skills": ["Python"], "completed_courses": []},
            "jobs": [{"title": "Backend Engineer", "company": "Acme", "required_skills": ["Python"], "covered": ["Python"], "gaps": []}],
            "courses": [],
        }
        entities = self._entities(bundle)
        citations = [{"claim": "good fit", "source": "machine learning engineer"}]
        violations = _validate_citations(citations, entities)
        self.assertTrue(len(violations) > 0)
        self.assertIn("machine learning engineer", violations[0])

    def test_citation_pointing_to_real_course_code_is_allowed(self):
        bundle = {
            "student": {"skills": [], "completed_courses": []},
            "jobs": [],
            "courses": [{"course_code": "CSC 510", "title": "Machine Learning", "teaches": ["Machine Learning"]}],
        }
        entities = self._entities(bundle)
        citations = [{"claim": "closes your ML gap", "source": "csc 510"}]
        violations = _validate_citations(citations, entities)
        self.assertEqual(violations, [])

    def test_citation_pointing_to_invented_course_is_flagged(self):
        bundle = {
            "student": {"skills": [], "completed_courses": []},
            "jobs": [],
            "courses": [{"course_code": "CSC 510", "title": "Machine Learning", "teaches": ["Machine Learning"]}],
        }
        entities = self._entities(bundle)
        citations = [{"claim": "good course", "source": "deep learning systems"}]
        violations = _validate_citations(citations, entities)
        self.assertTrue(len(violations) > 0)

    def test_empty_citations_produce_no_violations(self):
        bundle = {
            "student": {"skills": [], "completed_courses": []},
            "jobs": [],
            "courses": [],
        }
        entities = self._entities(bundle)
        violations = _validate_citations([], entities)
        self.assertEqual(violations, [])

    def test_citation_with_empty_source_is_ignored(self):
        bundle = {
            "student": {"skills": [], "completed_courses": []},
            "jobs": [],
            "courses": [],
        }
        entities = self._entities(bundle)
        violations = _validate_citations([{"claim": "something", "source": ""}], entities)
        self.assertEqual(violations, [])


class DeterministicGuardrailTests(unittest.TestCase):
    """Tests for phrase-match guards that were kept in _deterministic_support_checks."""

    def test_plain_english_at_does_not_trigger_company_mismatch(self):
        bundle = {
            "student": {"skills": ["Python"], "completed_courses": []},
            "jobs": [
                {
                    "title": "Backend Engineer",
                    "company": "Acme",
                    "required_skills": ["Python", "Distributed Systems"],
                    "covered": ["Python"],
                    "gaps": ["Distributed Systems"],
                }
            ],
            "courses": [],
        }
        result = critique_candidate(
            question="What should I learn next?",
            bundle=bundle,
            context="Backend Engineer at Acme requires Distributed Systems.",
            response="You should look at distributed systems next.",
        )
        self.assertFalse(any("company references do not align" in finding for finding in result["support_findings"]))

    def test_non_retrieved_resource_suggestion_is_penalized(self):
        bundle = {
            "student": {"skills": ["Python"], "completed_courses": []},
            "jobs": [{"title": "Backend Engineer", "company": "Acme", "required_skills": ["Python"], "covered": ["Python"], "gaps": []}],
            "courses": [],
        }
        result = critique_candidate(
            question="How can I improve?",
            bundle=bundle,
            context="Backend Engineer at Acme requires Python.",
            response="You could also take an online resource to build these skills.",
        )
        self.assertTrue(any("non-retrieved learning resources" in finding for finding in result["support_findings"]))

    def test_unsupported_course_code_is_penalized(self):
        bundle = {
            "student": {"skills": [], "completed_courses": []},
            "jobs": [],
            "courses": [{"course_code": "CSC 510", "title": "Machine Learning", "teaches": ["Machine Learning"]}],
        }
        result = critique_candidate(
            question="What should I take?",
            bundle=bundle,
            context="CSC 510 Machine Learning.",
            response="Take CSC 999 to build your skills.",
        )
        self.assertTrue(any("unsupported course codes" in finding for finding in result["support_findings"]))

    def test_generic_skill_advice_does_not_trigger_false_positive(self):
        bundle = {
            "student": {"skills": ["Python"], "completed_courses": []},
            "jobs": [
                {
                    "title": "Backend Engineer",
                    "company": "Acme",
                    "required_skills": ["Python", "Distributed Systems"],
                    "covered": ["Python"],
                    "gaps": ["Distributed Systems"],
                }
            ],
            "courses": [],
        }
        result = critique_candidate(
            question="What should I learn next?",
            bundle=bundle,
            context="Backend Engineer at Acme requires Distributed Systems.",
            response="You should take distributed systems next.",
        )
        self.assertFalse(any("unsupported course codes" in finding for finding in result["support_findings"]))


if __name__ == "__main__":
    unittest.main()
