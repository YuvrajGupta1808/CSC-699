import unittest
from unittest.mock import patch

from retrieval.candidates import build_candidate_views
from retrieval.critique import critique_candidate
from retrieval.job_content import build_job_embedding_text, chunk_text, extract_job_skills
from retrieval.planner import plan_retrieval
from retrieval.skills import compute_skill_overlap, count_skill_overlap, normalize_skill_name


def _no_llm(question, history_summary):
    return None


class PlannerTests(unittest.TestCase):
    def _plan(self, question, history=None):
        with patch("retrieval.planner._llm_classify_intent", side_effect=_no_llm):
            return plan_retrieval(question, history)

    def test_greeting_skips_retrieval(self):
        result = self._plan("hello")
        self.assertEqual(result["intent"], "greeting")
        self.assertEqual(result["top_k_jobs"], 0)
        self.assertEqual(result["top_k_courses"], 0)

    def test_course_question_prefers_courses(self):
        result = self._plan("What courses should I take to learn machine learning?")
        self.assertIn(result["intent"], ("courses", "skill_gap"))
        self.assertGreaterEqual(result["top_k_courses"], 4)

    def test_role_skill_question_prefers_jobs(self):
        result = self._plan("What skills do I need for backend roles?")
        self.assertEqual(result["intent"], "jobs")
        self.assertEqual(result["top_k_jobs"], 6)
        self.assertEqual(result["top_k_courses"], 2)


class SkillNormalizationTests(unittest.TestCase):
    def test_aliases_normalize(self):
        self.assertEqual(normalize_skill_name("ML"), "machine learning")
        self.assertEqual(normalize_skill_name("Node.js"), "nodejs")

    def test_overlap_uses_normalized_skill_names(self):
        covered, gaps = compute_skill_overlap(
            ["Machine Learning", "Python", "C++"],
            ["ML", "python", "Databases"],
        )
        self.assertEqual(covered, ["Machine Learning", "Python"])
        self.assertEqual(gaps, ["C++"])

    def test_count_overlap_uses_normalized_skill_names(self):
        self.assertEqual(count_skill_overlap(["Node.js", "ML"], ["nodejs", "Machine Learning"]), 2)


class JobContentTests(unittest.TestCase):
    def test_extract_job_skills_captures_long_tail_terms(self):
        skills = extract_job_skills(
            "Applied AI Engineer",
            "Build customer support RAG systems with Python, GraphQL, MongoDB, and PyTorch.",
        )
        self.assertIn("Retrieval-Augmented Generation", skills)
        self.assertIn("GraphQL", skills)
        self.assertIn("MongoDB", skills)
        self.assertIn("PyTorch", skills)

    def test_chunk_text_preserves_late_content(self):
        text = "intro " * 350 + "tail-signal"
        chunks = chunk_text(text, max_chars=200, overlap=20)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(any("tail-signal" in chunk for chunk in chunks))

    def test_job_embedding_text_includes_structure(self):
        text = build_job_embedding_text(
            {
                "title": "Software Engineer",
                "company": "Acme",
                "location": "San Francisco, CA",
                "skills_jobs": ["Python", "GraphQL"],
                "description": "Build internal tooling.",
            }
        )
        self.assertIn("Job Title: Software Engineer", text)
        self.assertIn("Skills: Python, GraphQL", text)


class CandidateViewTests(unittest.TestCase):
    def test_specific_job_view_matches_normalized_course_skills(self):
        bundle = {
            "student": {"name": "Alex", "major": "CS", "skills": ["Python"], "completed_courses": []},
            "jobs": [
                {
                    "title": "ML Engineer",
                    "company": "Acme",
                    "gaps": ["ML", "Node.js"],
                    "required_skills": ["Machine Learning", "Node.js"],
                    "covered": ["Python"],
                    "score": 0.9,
                    "description_excerpt": "Build ML systems with Node.js services.",
                }
            ],
            "courses": [
                {
                    "course_code": "CSC 510",
                    "title": "Machine Learning",
                    "teaches": ["Machine Learning"],
                    "score": 0.8,
                    "description_excerpt": "Covers core ML methods.",
                },
                {
                    "course_code": "CSC 520",
                    "title": "Web APIs",
                    "teaches": ["nodejs"],
                    "score": 0.7,
                    "description_excerpt": "Build services using Node.js.",
                },
            ],
        }
        views = build_candidate_views(bundle)
        specific_job_context = views[0]["context"]
        self.assertIn("CSC 510", specific_job_context)
        self.assertIn("CSC 520", specific_job_context)
        self.assertIn("Addresses gaps: Machine Learning", specific_job_context)
        self.assertIn("Source excerpt (course description): Covers core ML methods.", specific_job_context)

    def test_specific_job_view_reports_when_no_course_supports_gap(self):
        bundle = {
            "student": {"name": "Alex", "major": "CS", "skills": ["Python"], "completed_courses": []},
            "jobs": [
                {
                    "title": "Distributed Systems Engineer",
                    "company": "Acme",
                    "gaps": ["Distributed Systems"],
                    "required_skills": ["Distributed Systems"],
                    "covered": [],
                    "score": 0.9,
                }
            ],
            "courses": [
                {"course_code": "CSC 101", "title": "Intro to Computing", "teaches": ["Java"], "score": 0.8},
            ],
        }
        views = build_candidate_views(bundle)
        specific_job_context = views[0]["context"]
        self.assertIn("No retrieved courses clearly address these gaps", specific_job_context)
        self.assertNotIn("CSC 101", specific_job_context)

    def test_course_only_bundle_keeps_multiple_courses_across_views(self):
        bundle = {
            "student": {"name": "Alex", "major": "CS", "skills": ["Python"], "completed_courses": []},
            "jobs": [],
            "courses": [
                {"course_code": "CSC 510", "title": "Machine Learning", "teaches": ["Machine Learning"], "score": 0.95},
                {"course_code": "CSC 520", "title": "Web APIs", "teaches": ["Node.js"], "score": 0.85},
                {"course_code": "CSC 530", "title": "Databases", "teaches": ["SQL"], "score": 0.75},
                {"course_code": "CSC 540", "title": "Distributed Systems", "teaches": ["Distributed Systems"], "score": 0.65},
            ],
        }
        views = build_candidate_views(bundle)
        self.assertIn("CSC 510", views[0]["context"])
        self.assertIn("CSC 520", views[0]["context"])
        self.assertIn("CSC 530", views[1]["context"])
        self.assertIn("CSC 540", views[2]["context"])

    def test_course_path_falls_back_to_top_courses_when_gap_support_is_sparse(self):
        bundle = {
            "student": {"name": "Alex", "major": "CS", "skills": ["Python"], "completed_courses": []},
            "jobs": [
                {
                    "title": "Backend Engineer",
                    "company": "Acme",
                    "gaps": ["Distributed Systems"],
                    "required_skills": ["Python", "Distributed Systems"],
                    "covered": ["Python"],
                    "score": 0.92,
                }
            ],
            "courses": [
                {"course_code": "CSC 101", "title": "Intro to Computing", "teaches": ["Java"], "score": 0.9},
                {"course_code": "CSC 220", "title": "Data Structures", "teaches": ["Algorithms"], "score": 0.8},
            ],
        }
        views = build_candidate_views(bundle)
        self.assertIn("No retrieved courses clearly address the top combined gaps", views[2]["context"])
        self.assertIn("CSC 101", views[2]["context"])
        self.assertIn("CSC 220", views[2]["context"])


class CritiqueTests(unittest.TestCase):
    def test_unsupported_course_code_is_penalized(self):
        bundle = {
            "student": {"skills": ["Python"], "completed_courses": ["CSC 220"]},
            "jobs": [
                {
                    "title": "Machine Learning Engineer",
                    "company": "Acme",
                    "required_skills": ["Python", "Machine Learning"],
                    "covered": ["Python"],
                    "gaps": ["Machine Learning"],
                }
            ],
            "courses": [
                {"course_code": "CSC 510", "title": "Machine Learning", "teaches": ["Machine Learning"]}
            ],
        }
        result = critique_candidate(
            question="What should I learn next?",
            bundle=bundle,
            context="Machine Learning Engineer at Acme. CSC 510 teaches Machine Learning.",
            response="You should take CSC 999 and target Machine Learning Engineer roles.",
        )
        self.assertLessEqual(result["support"], 8)
        self.assertTrue(any("unsupported course codes" in finding for finding in result["support_findings"]))

    def test_completed_course_reference_is_allowed(self):
        bundle = {
            "student": {"skills": ["Python"], "completed_courses": ["CSC 220"]},
            "jobs": [],
            "courses": [],
        }
        result = critique_candidate(
            question="What parts of my background are relevant?",
            bundle=bundle,
            context="Student completed CSC 220 and has Python skills.",
            response="Your completed course CSC 220 is relevant background for this question.",
        )
        self.assertFalse(any("unsupported course codes" in finding for finding in result["support_findings"]))

    def test_nonretrieved_learning_resource_is_penalized(self):
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
            "courses": [
                {
                    "course_code": "CSC 847",
                    "title": "Cloud and Distributed Computing",
                    "teaches": ["Distributed Systems"],
                    "addresses_gaps": ["Distributed Systems"],
                }
            ],
        }
        result = critique_candidate(
            question="What should I learn next?",
            bundle=bundle,
            context="Backend Engineer at Acme. CSC 847 addresses Distributed Systems.",
            response="Take CSC 847. Alternatively, you could also use an online resource for Distributed Systems.",
        )
        self.assertTrue(any("non-retrieved learning resources" in finding for finding in result["support_findings"]))

    def test_contradicting_job_requirement_is_penalized(self):
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
            context="Backend Engineer at Acme requires Python and Distributed Systems.",
            response="Distributed Systems is not required for these job postings.",
        )
        self.assertTrue(any("contradicts retrieved job requirements" in finding for finding in result["support_findings"]))

    def test_retrieved_course_without_gap_support_is_penalized(self):
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
            "courses": [
                {
                    "course_code": "CSC 101",
                    "title": "Intro to Computing",
                    "teaches": ["Java"],
                    "addresses_gaps": [],
                }
            ],
        }
        result = critique_candidate(
            question="What course should I take next?",
            bundle=bundle,
            context="CSC 101 teaches Java.",
            response="Take CSC 101 next.",
        )
        self.assertTrue(any("course recommendation lacks gap support" in finding for finding in result["support_findings"]))


if __name__ == "__main__":
    unittest.main()
