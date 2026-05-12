"""
gold_questions.py — Canonical high-quality test queries representing the system's
intended use cases. These questions are what a real CS student would ask, grounded
in actual student profiles, real job titles, and real course codes from the database.

Run:
  cd server && ../.venv/bin/python tests/gold_questions.py

Outputs:
  tests/gold_results.md
"""

import sys
import time
import textwrap
from datetime import datetime
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")

from retrieval.graph import run_advisor_turn

# ── Student IDs ────────────────────────────────────────────────────────────────
# Alex Chen   — CS major, foundational skills (Python, Java, DS, Algorithms, OOP)
#               Completed: CSC 101, 220, 315, 340
ALEX  = "00000000-0000-0000-0000-000000000001"

# Maria Gomez — CS major, strong ML/data profile (ML, Python, DBs, OS, DL, SQL)
#               Completed: CSC 220, 415, 510, 600, 667
MARIA = "00000000-0000-0000-0000-000000000002"

# Sam Patel   — CS major, entry-level (Java, Programming Fundamentals, Computational Thinking)
#               Completed: CSC 101, 110, 215
SAM     = "00000000-0000-0000-0000-000000000003"

# Jordan Kim  — CS senior, strong full-stack (Python, JS, TS, React, Node, SQL, Docker, CI/CD)
#               Completed: CSC 220, 317, 340, 413, 648, 667, 675
JORDAN  = "00000000-0000-0000-0000-000000000004"

# Marcus Webb — CS senior, cloud/DevOps focus (Python, AWS, Docker, K8s, Terraform, Go, CI/CD)
#               Completed: CSC 220, 415, 645, 647, 651, 652, 746
MARCUS  = "00000000-0000-0000-0000-000000000005"

# Taylor Reyes — CS grad student, ML/AI specialist (PyTorch, TF, CV, LLMs, NLP, DL)
#                Completed: CSC 415, 510, 603, 620, 665, 671, 675, 805
TAYLOR  = "00000000-0000-0000-0000-000000000006"

# Priya Sharma — CS/Biology double major, data science (Python, R, ML, Bioinformatics, SQL)
#                Completed: CSC 311, 408, 411, 509, 511, 601, 657, 805
PRIYA   = "00000000-0000-0000-0000-000000000007"

# ── Gold question definitions ──────────────────────────────────────────────────
# Each entry:
#   id          — unique identifier
#   category    — thematic group
#   student_id  — which student asks it
#   student     — human-readable student label
#   message     — the actual query
#   rationale   — why this is a gold question (what it tests)
#   eval_criteria — what a good answer must include

GOLD_QUESTIONS = [
    # ── 1. Specific Job Fit ─────────────────────────────────────────────────
    {
        "id": "GQ-01",
        "category": "Specific Job Fit",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "Am I a good fit for the Junior Software Engineer role at Leidos?",
        "rationale": "Tests whether the system retrieves a specific named job and computes Alex's exact gap for it.",
        "eval_criteria": "Must reference Leidos by name, list Alex's covered and gap skills specifically.",
    },
    {
        "id": "GQ-02",
        "category": "Specific Job Fit",
        "student_id": MARIA,
        "student": "Maria Gomez",
        "message": "Which ML engineering jobs match my profile and what's missing?",
        "rationale": "Maria has ML/DL skills — tests whether the system retrieves ML-relevant roles and accurately identifies remaining gaps.",
        "eval_criteria": "Should surface ML-relevant roles, use Maria's actual skill set, list specific gaps.",
    },
    {
        "id": "GQ-03",
        "category": "Specific Job Fit",
        "student_id": SAM,
        "student": "Sam Patel",
        "message": "I only have basic programming skills. What entry-level jobs are realistic for me right now?",
        "rationale": "Sam has minimal skills — tests realistic expectation setting for an underprepared student.",
        "eval_criteria": "Should not oversell Sam's readiness; should name specific achievable jobs and list actual gaps honestly.",
    },

    # ── 2. Skill Gap Analysis ───────────────────────────────────────────────
    {
        "id": "GQ-04",
        "category": "Skill Gap Analysis",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "What specific skills am I missing to qualify for a full stack engineering role?",
        "rationale": "Tests extraction of full-stack-specific gap skills from retrieved job evidence.",
        "eval_criteria": "Must name concrete missing skills (e.g. JavaScript, React, SQL) grounded in job evidence.",
    },
    {
        "id": "GQ-05",
        "category": "Skill Gap Analysis",
        "student_id": MARIA,
        "student": "Maria Gomez",
        "message": "I'm strong in ML and deep learning. What gaps are blocking me from cloud engineering roles?",
        "rationale": "Tests cross-domain gap detection — Maria's ML profile vs cloud requirements.",
        "eval_criteria": "Should identify cloud-specific gaps (GCP, AWS, Terraform, etc.) not covered by Maria's ML background.",
    },
    {
        "id": "GQ-06",
        "category": "Skill Gap Analysis",
        "student_id": SAM,
        "student": "Sam Patel",
        "message": "What is the single most important skill I should learn next to become more employable?",
        "rationale": "Tests prioritized advice — system should pick one concrete skill with justification from evidence.",
        "eval_criteria": "Must name one specific skill with supporting job evidence, not a generic list.",
    },

    # ── 3. Course Recommendation ────────────────────────────────────────────
    {
        "id": "GQ-07",
        "category": "Course Recommendation",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "Which courses should I take to become competitive for web development jobs?",
        "rationale": "Tests course retrieval for a specific domain — web dev — with course code citation.",
        "eval_criteria": "Must cite actual course codes (e.g. CSC 307, CSC 317) and explain which gap each addresses.",
    },
    {
        "id": "GQ-08",
        "category": "Course Recommendation",
        "student_id": SAM,
        "student": "Sam Patel",
        "message": "What's the most valuable course I can take next semester to open up more job options?",
        "rationale": "Tests highest-impact course recommendation for a beginner student.",
        "eval_criteria": "Must name a specific course code and explain which job gaps it closes.",
    },
    {
        "id": "GQ-09",
        "category": "Course Recommendation",
        "student_id": MARIA,
        "student": "Maria Gomez",
        "message": "I've already taken CSC 415 and CSC 510. What advanced courses build on those for AI roles?",
        "rationale": "Tests awareness of completed courses and progression recommendations.",
        "eval_criteria": "Should not recommend CSC 415/510 again; should suggest genuinely next-level courses for AI.",
    },

    # ── 4. Career Readiness & Broad Analysis ───────────────────────────────
    {
        "id": "GQ-10",
        "category": "Career Readiness",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "I'm graduating in 6 months. Give me an honest assessment of my job market readiness.",
        "rationale": "Tests broad readiness analysis — should balance encouragement with honest gap identification.",
        "eval_criteria": "Must be grounded in Alex's actual skills, name real jobs, not claim readiness for roles he can't fill.",
    },
    {
        "id": "GQ-11",
        "category": "Career Readiness",
        "student_id": MARIA,
        "student": "Maria Gomez",
        "message": "Create a semester-by-semester plan to make me competitive for senior ML roles.",
        "rationale": "Tests multi-step planning grounded in available courses and job requirements.",
        "eval_criteria": "Must use real course codes, real job titles from evidence; should not invent steps or skills.",
    },
    {
        "id": "GQ-12",
        "category": "Career Readiness",
        "student_id": SAM,
        "student": "Sam Patel",
        "message": "Be honest — am I competitive for any real industry jobs right now?",
        "rationale": "Tests candid honest assessment for a weak profile without being discouraging.",
        "eval_criteria": "Should not invent optimism — must reflect Sam's limited skill set accurately while pointing to a path forward.",
    },

    # ── 5. Job Comparison ──────────────────────────────────────────────────
    {
        "id": "GQ-13",
        "category": "Job Comparison",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "Between a software engineering role at Microsoft and one at a startup like Giga, which is a better fit for where I am now?",
        "rationale": "Tests comparative multi-job reasoning — system must assess Alex against two different role profiles.",
        "eval_criteria": "Must compare both companies using evidence; should not fabricate requirements not in retrieved data.",
    },
    {
        "id": "GQ-14",
        "category": "Job Comparison",
        "student_id": MARIA,
        "student": "Maria Gomez",
        "message": "Which pays off more for my career — taking more ML courses or pivoting to cloud/DevOps?",
        "rationale": "Tests strategic advice grounded in job evidence — system must compare both paths using retrieved data.",
        "eval_criteria": "Must use retrieved job and course evidence; must not speculate beyond the evidence.",
    },

    # ── 6. Action-Oriented ─────────────────────────────────────────────────
    {
        "id": "GQ-15",
        "category": "Action Plan",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "What are the top 3 most impactful things I can do this semester to improve my job prospects?",
        "rationale": "Tests synthesis into concrete action items — courses + skill targets grounded in evidence.",
        "eval_criteria": "Must produce exactly 3 items; each item must map to real evidence (course codes or specific job gaps).",
    },
    {
        "id": "GQ-16",
        "category": "Action Plan",
        "student_id": SAM,
        "student": "Sam Patel",
        "message": "If I can only take one more course, which one gives me the best shot at getting hired?",
        "rationale": "Tests forced single-best-choice recommendation with full justification.",
        "eval_criteria": "Must name one specific course code and explain concretely why that course beats the alternatives.",
    },

    # ── 7. Domain Pivot ────────────────────────────────────────────────────
    {
        "id": "GQ-17",
        "category": "Domain Pivot",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "I want to pivot into data science. What's the gap between where I am and data science jobs?",
        "rationale": "Tests gap analysis for a domain pivot — Alex's current profile vs data science requirements.",
        "eval_criteria": "Must identify specific data science skills (ML, SQL, stats, etc.) missing from Alex's profile.",
    },
    {
        "id": "GQ-18",
        "category": "Domain Pivot",
        "student_id": MARIA,
        "student": "Maria Gomez",
        "message": "I'm thinking of moving into systems or embedded software. Is my background relevant at all?",
        "rationale": "Tests cross-domain relevance check — ML background vs systems engineering requirements.",
        "eval_criteria": "Must assess Maria's actual skills against systems requirements; should not fabricate overlap.",
    },

    # ── 8. Self-Assessment ─────────────────────────────────────────────────
    {
        "id": "GQ-19",
        "category": "Self-Assessment",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "What are my strongest marketable skills and which job category do they point toward?",
        "rationale": "Tests skill-to-job-category mapping for the student's actual skills.",
        "eval_criteria": "Must reference Alex's real skills (Python, Java, DS, Algorithms); must point to specific job categories from evidence.",
    },
    {
        "id": "GQ-20",
        "category": "Self-Assessment",
        "student_id": MARIA,
        "student": "Maria Gomez",
        "message": "Given everything I've learned, what kind of engineer am I becoming and what should I double down on?",
        "rationale": "Tests identity/trajectory synthesis from profile data — Maria's ML-heavy background.",
        "eval_criteria": "Should identify Maria's ML/data trajectory explicitly, recommend courses or job directions that deepen it.",
    },

    # ── 9. Strong-Fit Validation (new diverse students) ────────────────────
    {
        "id": "GQ-21",
        "category": "Strong Fit",
        "student_id": JORDAN,
        "student": "Jordan Kim",
        "message": "What full stack or web engineering roles am I competitive for right now?",
        "rationale": "Jordan has 15 web-relevant skills — tests whether the system recognizes a strong fit and shrinks the gap list accordingly.",
        "eval_criteria": "Should show high skill coverage (≥50%), short gap list, and name specific web/full-stack roles.",
    },
    {
        "id": "GQ-22",
        "category": "Strong Fit",
        "student_id": MARCUS,
        "student": "Marcus Webb",
        "message": "Am I ready for a cloud or DevOps engineering role?",
        "rationale": "Marcus has 14 cloud/DevOps skills — tests whether the system correctly identifies near-readiness and gives a precise, short gap list.",
        "eval_criteria": "Should show high coverage for cloud roles, list specific remaining gaps (e.g. Azure, GCP), not generic advice.",
    },
    {
        "id": "GQ-23",
        "category": "Strong Fit",
        "student_id": TAYLOR,
        "student": "Taylor Reyes",
        "message": "Which ML or AI research engineering positions am I closest to qualifying for?",
        "rationale": "Taylor has 16 ML/AI skills — tests whether the system identifies near-qualified ML roles and produces a tight gap list.",
        "eval_criteria": "Should name ML/AI specific roles, show strong coverage, list only a few remaining gaps.",
    },

    # ── 10. Cross-Disciplinary (Priya) ─────────────────────────────────────
    {
        "id": "GQ-24",
        "category": "Cross-Disciplinary",
        "student_id": PRIYA,
        "student": "Priya Sharma",
        "message": "Given my biology and CS background, what unique job opportunities exist for me?",
        "rationale": "Priya is a CS/Biology double major — tests whether the system surfaces bioinformatics/biotech roles and treats her interdisciplinary background as an advantage.",
        "eval_criteria": "Should reference bioinformatics or biotech-adjacent roles; must not treat her as a generic CS student.",
    },
    {
        "id": "GQ-25",
        "category": "Cross-Disciplinary",
        "student_id": PRIYA,
        "student": "Priya Sharma",
        "message": "Which courses would strengthen my data science skills specifically for biomedical research?",
        "rationale": "Tests domain-specific course recommendations for a niche interdisciplinary student.",
        "eval_criteria": "Should recommend courses relevant to biomedical data (CSC 509, 511, 621, 657 etc.); must cite course codes.",
    },

    # ── 11. Skill-Gap Intent (exercises new planner invariant: jobs + courses) ─
    {
        "id": "GQ-26",
        "category": "Skill Gap with Job Context",
        "student_id": JORDAN,
        "student": "Jordan Kim",
        "message": "What skills am I missing to land a senior software engineer role?",
        "rationale": "Targets the new skill_gap intent which must retrieve ≥3 jobs alongside courses — tests the invariant that gap analysis is grounded in job evidence, not just general learning advice.",
        "eval_criteria": "Must reference specific retrieved job roles, list Jordan's actual gaps (e.g. system design, cloud), and recommend courses by code.",
    },
    {
        "id": "GQ-27",
        "category": "Skill Gap with Job Context",
        "student_id": MARCUS,
        "student": "Marcus Webb",
        "message": "I want to move into ML engineering — what's the gap between my DevOps background and those roles?",
        "rationale": "Cross-domain gap test: Marcus has cloud/DevOps skills; asking about ML engineering should retrieve ML-specific job evidence and identify missing ML skills.",
        "eval_criteria": "Must identify ML-specific gaps from retrieved job evidence (PyTorch, TF, model training, etc.); should not conflate DevOps overlap with ML readiness.",
    },
    {
        "id": "GQ-28",
        "category": "Skill Gap with Job Context",
        "student_id": TAYLOR,
        "student": "Taylor Reyes",
        "message": "What skills do I still need to qualify for production ML engineering at a top tech company?",
        "rationale": "Taylor has deep research ML skills — tests whether the system identifies the research-to-production gap (MLOps, deployment, distributed training, system design).",
        "eval_criteria": "Must surface production/MLOps gaps (e.g. Kubernetes, MLflow, distributed training) grounded in job evidence; should not suggest research courses Taylor already has.",
    },

    # ── 12. Retrieval Precision (narrow intent) ────────────────────────────
    {
        "id": "GQ-29",
        "category": "Retrieval Precision",
        "student_id": ALEX,
        "student": "Alex Chen",
        "message": "What Python-specific courses do I still need?",
        "rationale": "Narrow query — should retrieve Python-teaching courses specifically, not generic CS courses. Tests whether the course query is tightly scoped to user intent.",
        "eval_criteria": "Must recommend only courses that teach Python or Python-adjacent skills; must cite course codes; should not recommend unrelated courses.",
    },
    {
        "id": "GQ-30",
        "category": "Retrieval Precision",
        "student_id": SAM,
        "student": "Sam Patel",
        "message": "Are there any jobs that only require Java?",
        "rationale": "Tests whether the system can identify a narrow requirement filter — jobs whose coverage is achievable with just Java skills. Tests precision over recall.",
        "eval_criteria": "Should name specific roles where Java alone (or with basic skills Sam has) meets a majority of requirements; must ground in retrieved job evidence.",
    },
]


# ── Runner ─────────────────────────────────────────────────────────────────────

def run_gold_question(gq: dict) -> dict:
    print(f"\n{'=' * 72}")
    print(f"[{gq['id']}] {gq['category']} — {gq['student']}")
    print(f"  Q: {gq['message']}")

    t0 = time.time()
    try:
        result = run_advisor_turn(
            user_message=gq["message"],
            student_id=gq["student_id"],
            conversation_history=[],
            session_id=f"gold-{gq['id']}-{uuid4()}",
        )
        elapsed = round(time.time() - t0, 1)

        plan = result.get("plan", {})
        best = result.get("best_candidate", {})
        scores = best.get("scores", {})
        response = result.get("final_response", "")
        status_log = result.get("status_log", [])

        print(f"  Intent : {plan.get('intent')} | K: jobs={plan.get('top_k_jobs')} courses={plan.get('top_k_courses')}")
        print(f"  Scores : {scores.get('relevance')}/10 relevance  {scores.get('support')}/10 support  {scores.get('utility')}/10 utility  → total {scores.get('total')}")
        print(f"  Time   : {elapsed}s")
        print(f"  Log    : {' → '.join(status_log)}")
        print(f"\n  RESPONSE:\n{textwrap.fill(response[:800], width=80, initial_indent='  ', subsequent_indent='  ')}")

        return {
            "id": gq["id"],
            "category": gq["category"],
            "student": gq["student"],
            "message": gq["message"],
            "rationale": gq["rationale"],
            "eval_criteria": gq["eval_criteria"],
            "status": "ok",
            "elapsed_s": elapsed,
            "intent": plan.get("intent"),
            "top_k_jobs": plan.get("top_k_jobs"),
            "top_k_courses": plan.get("top_k_courses"),
            "plan_reason": plan.get("reason"),
            "scores": scores,
            "response": response,
            "status_log": status_log,
            "critique": scores.get("critique", ""),
            "support_findings": scores.get("support_findings", []),
        }

    except Exception as exc:
        elapsed = round(time.time() - t0, 1)
        print(f"  ERROR: {exc}")
        return {
            "id": gq["id"],
            "category": gq["category"],
            "student": gq["student"],
            "message": gq["message"],
            "rationale": gq["rationale"],
            "eval_criteria": gq["eval_criteria"],
            "status": "error",
            "elapsed_s": elapsed,
            "error": str(exc),
        }


# ── Markdown report generation ─────────────────────────────────────────────────

def score_emoji(score: float | None) -> str:
    if score is None:
        return "—"
    if score >= 8:
        return "🟢"
    if score >= 6:
        return "🟡"
    return "🔴"


def generate_markdown(results: list[dict], run_at: str) -> str:
    lines = []
    lines.append("# Gold Question Evaluation Report")
    lines.append(f"\n**Run date:** {run_at}")
    lines.append(f"**Total questions:** {len(results)}")
    lines.append(f"**System:** LangGraph advisor · Ollama (llama3.2) · Qdrant + Supabase")
    lines.append("")

    # Summary table
    ok = [r for r in results if r["status"] == "ok"]
    errors = [r for r in results if r["status"] == "error"]
    avg_total = round(sum(r["scores"].get("total", 0) for r in ok) / len(ok), 2) if ok else 0
    avg_time = round(sum(r["elapsed_s"] for r in ok) / len(ok), 1) if ok else 0

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Passed | {len(ok)}/{len(results)} |")
    lines.append(f"| Errors | {len(errors)} |")
    lines.append(f"| Average score | {avg_total}/10 |")
    lines.append(f"| Average time | {avg_time}s |")
    lines.append(f"| Score legend | 🟢 ≥8 · 🟡 ≥6 · 🔴 <6 |")
    lines.append("")

    # Score table
    lines.append("## Scores At a Glance")
    lines.append("")
    lines.append("| ID | Category | Student | Intent | Rel | Sup | Util | **Total** | Time |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in results:
        if r["status"] == "error":
            lines.append(f"| {r['id']} | {r['category']} | {r['student']} | — | — | — | — | **ERROR** | {r['elapsed_s']}s |")
            continue
        s = r["scores"]
        total = s.get("total", 0)
        em = score_emoji(total)
        lines.append(
            f"| {r['id']} | {r['category']} | {r['student']} | `{r['intent']}` "
            f"| {s.get('relevance','—')} | {s.get('support','—')} | {s.get('utility','—')} "
            f"| {em} **{total}** | {r['elapsed_s']}s |"
        )
    lines.append("")

    # Per-question detail
    lines.append("---")
    lines.append("")
    lines.append("## Question-by-Question Results")
    lines.append("")

    by_category: dict[str, list[dict]] = {}
    for r in results:
        by_category.setdefault(r["category"], []).append(r)

    for category, cat_results in by_category.items():
        lines.append(f"### {category}")
        lines.append("")

        for r in cat_results:
            lines.append(f"#### {r['id']} — {r['student']}")
            lines.append("")
            lines.append(f"**Query:** _{r['message']}_")
            lines.append("")
            lines.append(f"**Rationale:** {r['rationale']}")
            lines.append("")
            lines.append(f"**Expected:** {r['eval_criteria']}")
            lines.append("")

            if r["status"] == "error":
                lines.append(f"> ❌ **ERROR:** {r.get('error', 'unknown')}")
                lines.append("")
                continue

            s = r["scores"]
            total = s.get("total", 0)
            em = score_emoji(total)

            lines.append(f"| Field | Value |")
            lines.append(f"|---|---|")
            lines.append(f"| Intent | `{r['intent']}` (jobs={r['top_k_jobs']}, courses={r['top_k_courses']}) |")
            lines.append(f"| Planner reason | {r['plan_reason']} |")
            lines.append(f"| Relevance | {s.get('relevance', '—')}/10 |")
            lines.append(f"| Support | {s.get('support', '—')}/10 |")
            lines.append(f"| Utility | {s.get('utility', '—')}/10 |")
            lines.append(f"| **Total** | {em} **{total}/10** |")
            lines.append(f"| Time | {r['elapsed_s']}s |")
            lines.append("")

            if r.get("support_findings"):
                lines.append("**Critique flags:**")
                for flag in r["support_findings"]:
                    lines.append(f"- ⚠️ {flag}")
                lines.append("")

            critique_text = s.get("critique", "").split("|")[0].strip()
            if critique_text:
                lines.append(f"**Critique summary:** {critique_text}")
                lines.append("")

            lines.append("**Response:**")
            lines.append("")
            lines.append(f"> {r['response'][:1000].replace(chr(10), chr(10) + '> ')}")
            lines.append("")
            lines.append("---")
            lines.append("")

    # Findings section
    lines.append("## Key Findings")
    lines.append("")

    high_scorers = sorted([r for r in ok if r["scores"].get("total", 0) >= 8], key=lambda x: -x["scores"]["total"])
    low_scorers = sorted([r for r in ok if r["scores"].get("total", 0) < 6], key=lambda x: x["scores"]["total"])
    all_flags = []
    for r in ok:
        for flag in r.get("support_findings", []):
            all_flags.append((r["id"], flag))

    lines.append("### Top Performers (score ≥ 8)")
    if high_scorers:
        for r in high_scorers:
            lines.append(f"- **{r['id']}** ({r['category']}, {r['student']}): {r['scores']['total']}/10 — _{r['message'][:80]}_")
    else:
        lines.append("- None reached ≥ 8 in this run.")
    lines.append("")

    lines.append("### Needs Work (score < 6)")
    if low_scorers:
        for r in low_scorers:
            lines.append(f"- **{r['id']}** ({r['category']}, {r['student']}): {r['scores']['total']}/10 — _{r['message'][:80]}_")
    else:
        lines.append("- All questions scored ≥ 6.")
    lines.append("")

    lines.append("### Recurring Critique Flags")
    flag_counts: dict[str, int] = {}
    for _, flag in all_flags:
        normalized = flag.split(":")[0].strip()
        flag_counts[normalized] = flag_counts.get(normalized, 0) + 1
    if flag_counts:
        for flag, count in sorted(flag_counts.items(), key=lambda x: -x[1]):
            lines.append(f"- `{flag}` — appeared {count}×")
    else:
        lines.append("- No recurring flags.")
    lines.append("")

    lines.append("### Slow Queries (> 40s)")
    slow = [r for r in ok if r["elapsed_s"] > 40]
    if slow:
        for r in slow:
            lines.append(f"- **{r['id']}**: {r['elapsed_s']}s — {r['message'][:70]}")
    else:
        lines.append("- All queries completed in under 40s.")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Gold Question Evaluation — Career Advisor System")
    print("=" * 72)
    run_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    results = []
    for gq in GOLD_QUESTIONS:
        result = run_gold_question(gq)
        results.append(result)

    # Write markdown report
    md = generate_markdown(results, run_at)
    out_path = Path(__file__).parent / "gold_results.md"
    out_path.write_text(md, encoding="utf-8")

    print(f"\n\n{'#' * 72}")
    print("# GOLD QUESTION SUMMARY")
    print(f"{'#' * 72}\n")
    ok = [r for r in results if r["status"] == "ok"]
    errors = [r for r in results if r["status"] == "error"]
    print(f"Total    : {len(results)}")
    print(f"OK       : {len(ok)}")
    print(f"Errors   : {len(errors)}")
    if ok:
        avg = round(sum(r["scores"].get("total", 0) for r in ok) / len(ok), 2)
        print(f"Avg score: {avg}/10")
    print(f"\nMarkdown report written to: {out_path}")
