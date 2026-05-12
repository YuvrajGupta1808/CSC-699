import json
import re
from pathlib import Path
from time import perf_counter

from retrieval.context_builder import get_all_students
from retrieval.graph import run_advisor_turn


def _sanitize_preview(text: str, limit: int = 180) -> str:
    compact = " ".join((text or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _contains_unsupported_placeholder(text: str) -> bool:
    lowered = (text or "").lower()
    return "[insert" in lowered or "placeholder" in lowered


def _evaluate_turn(result: dict, expects_retrieval: bool) -> tuple[bool, list[str]]:
    failures: list[str] = []
    response = result.get("final_response", "") or ""
    plan = result.get("plan") or {}
    bundle = result.get("bundle") or {}
    best_candidate = result.get("best_candidate") or {}
    scores = best_candidate.get("scores") or {}
    jobs = bundle.get("jobs") or []
    courses = bundle.get("courses") or []

    if not response.strip():
        failures.append("empty response")
    if _contains_unsupported_placeholder(response):
        failures.append("placeholder text in response")

    if expects_retrieval:
        if plan.get("intent") == "greeting":
            failures.append("planner treated task as greeting")
        if not jobs and not courses:
            failures.append("no retrieved evidence")
        if scores.get("support", 0) < 7:
            failures.append("low support score")
        if scores.get("support_findings"):
            failures.append("support findings present")
    else:
        if plan.get("intent") != "greeting":
            failures.append("greeting did not route to greeting intent")

    return (len(failures) == 0), failures


def run_live_conversation_eval() -> tuple[int, int]:
    fixtures_path = Path(__file__).with_name("live_conversation_fixtures.json")
    fixtures = json.loads(fixtures_path.read_text())
    students = get_all_students()

    passed = 0
    total = 0

    for student in students:
        student_name = student["name"]
        student_id = student["student_id"]
        session_id = f"live-eval-{student_id}"
        conversation_history: list[dict[str, str]] = []

        print(f"\n=== Student: {student_name} ===")
        for case in fixtures:
            total += 1
            started = perf_counter()
            try:
                result = run_advisor_turn(
                    user_message=case["question"],
                    student_id=student_id,
                    conversation_history=conversation_history,
                    session_id=session_id,
                )
                elapsed = perf_counter() - started
                ok, failures = _evaluate_turn(result, case["expects_retrieval"])
                status = "PASS" if ok else "FAIL"
                preview = _sanitize_preview(result.get("final_response", ""))
                plan = result.get("plan") or {}
                bundle = result.get("bundle") or {}
                print(
                    f"[{status}] {case['name']} | "
                    f"intent={plan.get('intent')} jobs={len(bundle.get('jobs') or [])} "
                    f"courses={len(bundle.get('courses') or [])} "
                    f"time={elapsed:.1f}s"
                )
                print(f"  Q: {case['question']}")
                print(f"  A: {preview}")
                if failures:
                    print(f"  Issues: {', '.join(failures)}")
                if ok:
                    passed += 1
                    conversation_history.extend(
                        [
                            {"role": "user", "content": case["question"]},
                            {"role": "assistant", "content": result.get("final_response", "")},
                        ]
                    )
            except Exception as exc:
                elapsed = perf_counter() - started
                print(f"[FAIL] {case['name']} | exception after {elapsed:.1f}s")
                print(f"  Q: {case['question']}")
                print(f"  Issues: {type(exc).__name__}: {exc}")

    print(f"\nLive conversation eval: {passed}/{total} passed")
    return passed, total


if __name__ == "__main__":
    passed, total = run_live_conversation_eval()
    raise SystemExit(0 if passed == total else 1)
