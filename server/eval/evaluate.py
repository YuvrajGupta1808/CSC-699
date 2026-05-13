import json
from pathlib import Path

from retrieval.candidates import build_candidate_views
from retrieval.job_content import extract_job_skills
from retrieval.planner import plan_retrieval


def _planner_matches(result: dict, expected: dict) -> bool:
    """Support both exact values and _min thresholds in fixtures."""
    jobs_ok = (
        result["top_k_jobs"] >= expected["top_k_jobs_min"]
        if "top_k_jobs_min" in expected
        else result["top_k_jobs"] == expected["top_k_jobs"]
    )
    courses_ok = (
        result["top_k_courses"] >= expected["top_k_courses_min"]
        if "top_k_courses_min" in expected
        else result["top_k_courses"] == expected["top_k_courses"]
    )
    intent_ok = (
        result["intent"] == expected["intent"]
        if "intent" in expected
        else True
    )
    return jobs_ok and courses_ok and intent_ok


def run_planner_eval() -> tuple[int, int]:
    fixture_path = Path(__file__).with_name("golden_queries.json")
    fixtures = json.loads(fixture_path.read_text())
    passed = 0

    for case in fixtures:
        result = plan_retrieval(case["question"])
        ok = _planner_matches(result, case["expected"])
        status = "PASS" if ok else "FAIL"
        print(
            f"[{status}] {case['name']}: "
            f"got intent={result.get('intent')} jobs={result['top_k_jobs']} courses={result['top_k_courses']}"
        )
        if ok:
            passed += 1

    total = len(fixtures)
    print(f"\nPlanner eval: {passed}/{total} passed")
    return passed, total


def run_retrieval_logic_eval() -> tuple[int, int]:
    fixture_path = Path(__file__).with_name("retrieval_fixtures.json")
    fixtures = json.loads(fixture_path.read_text())
    passed = 0

    for case in fixtures:
        ok = False
        if case["kind"] == "planner":
            result = plan_retrieval(case["question"])
            ok = _planner_matches(result, case["expected"])
        elif case["kind"] == "job_skill_extraction":
            skills = extract_job_skills(case["title"], case["description"])
            ok = all(skill in skills for skill in case["expected_skills"])
        elif case["kind"] == "candidate_views":
            views = build_candidate_views(case["bundle"])
            specific_job_context = views[0]["context"]
            ok = all(code in specific_job_context for code in case["expected_course_codes"])

        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {case['name']}")
        if ok:
            passed += 1

    total = len(fixtures)
    print(f"\nRetrieval logic eval: {passed}/{total} passed")
    return passed, total


if __name__ == "__main__":
    planner_passed, planner_total = run_planner_eval()
    retrieval_passed, retrieval_total = run_retrieval_logic_eval()
    all_passed = planner_passed + retrieval_passed
    all_total = planner_total + retrieval_total
    print(f"\nOverall eval: {all_passed}/{all_total} passed")
    raise SystemExit(0 if all_passed == all_total else 1)
