"""
retrieval/critique.py

Scores each generated candidate on 3 axes:
  Relevance  — does it answer the user's actual question?
  Support    — are claims traceable to the evidence provided?
  Utility    — is the answer actionable with concrete next steps?

Support is enforced with deterministic evidence checks before any LLM score is used.
"""

import json
import os
import re

import httpx
from dotenv import load_dotenv

from retrieval.observability import ollama_timing_metadata, ollama_usage_metadata
from retrieval.prompts import CRITIQUE_PROMPT
from retrieval.skills import normalize_skill_name

load_dotenv()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.2")
# Critique uses a separate model to avoid self-evaluation bias.
# deepseek-r1 is a reasoning model with a different architecture than llama3.2.
CRITIQUE_MODEL = os.environ.get("OLLAMA_CRITIQUE_MODEL", "deepseek-r1:1.5b")

TITLE_CONNECTORS = (
    "and|or|of|for|to|in|on|with|the|a|an|vs|via|through|from"
)
TITLE_WORD_PATTERN = (
    rf"[A-Z][A-Za-z0-9/&+.#-]*"
    rf"(?:\s+(?:[A-Z][A-Za-z0-9/&+.#-]*|{TITLE_CONNECTORS}))*"
)
COMPANY_REFERENCE_PATTERN = re.compile(
    r"\bat\s+[A-Z][A-Za-z0-9&+.#-]*(?:\s+[A-Z][A-Za-z0-9&+.#-]*){0,3}\b"
)

# Words that commonly start sentences but are never job titles
_TITLE_SENTENCE_STARTERS = frozenset({
    "based", "according", "given", "as", "with", "in", "for", "to", "the",
    "this", "these", "those", "note", "however", "while", "since", "if",
    "when", "where", "because", "although", "additionally", "furthermore",
    "therefore", "thus", "overall", "currently", "specifically", "especially",
    "importantly", "unfortunately", "considering", "looking", "from", "by",
    "about", "there", "here", "both", "each", "all", "many", "most", "some",
    "two", "three", "four", "five", "please",
})

# Short tokens that are skills/languages, not course titles
_SKILL_TOKENS_NOT_COURSE_TITLES = frozenset({
    "python", "java", "go", "rust", "sql", "r", "c", "html", "css",
    "git", "aws", "gcp", "azure", "docker", "linux", "react", "vue",
    "node", "swift", "kotlin", "scala", "csc",
})

# Tokens that appear near skill-cue words but are not actual skills
_SKILL_STOP_WORDS = frozenset({
    "next", "is", "are", "the", "a", "an", "of", "to", "for", "in",
    "and", "or", "but", "not", "this", "that", "these", "those",
    "particularly", "concerning", "especially", "additionally",
})

# Generic phrase prefixes the critique LLM uses instead of exact entity names
_CITATION_META_PREFIXES = (
    "student profile", "student_profile", "evidence context", "relevant job",
    "relevant course", "the course description", "the job description",
    "the evidence", "source excerpt", "no course", "no skill",
)


def _allowed_entities(bundle: dict) -> dict[str, set[str]]:
    jobs = bundle.get("jobs", [])
    courses = bundle.get("courses", [])
    job_titles = {(job.get("title") or "").strip().lower() for job in jobs if job.get("title")}
    course_titles = {(course.get("title") or "").strip().lower() for course in courses if course.get("title")}
    companies = {(job.get("company") or "").strip().lower() for job in jobs if job.get("company")}
    course_codes = {(course.get("course_code") or "").strip().upper() for course in courses if course.get("course_code")}
    student_completed_courses = {
        (course_code or "").strip().upper()
        for course_code in bundle.get("student", {}).get("completed_courses", [])
        if course_code
    }
    allowed_skills = {
        normalize_skill_name(skill)
        for job in jobs
        for skill in job.get("required_skills", []) + job.get("covered", []) + job.get("gaps", [])
    }
    allowed_skills.update(
        normalize_skill_name(skill)
        for course in courses
        for skill in course.get("teaches", [])
    )
    allowed_skills.update(
        normalize_skill_name(skill)
        for skill in bundle.get("student", {}).get("skills", [])
    )
    return {
        "job_titles": {value for value in job_titles if value},
        "course_titles": {value for value in course_titles if value},
        "companies": {value for value in companies if value},
        "course_codes": {value for value in course_codes | student_completed_courses if value},
        "skills": {value for value in allowed_skills if value},
    }


def _extract_claimed_job_titles(response: str) -> set[str]:
    titles: set[str] = set()
    patterns = [
        re.compile(rf"\b({TITLE_WORD_PATTERN})\s+at\s+[A-Z]"),
        re.compile(rf"\b(?:The\s+)?({TITLE_WORD_PATTERN})\s+(?:role|position|job)\b"),
    ]
    for pattern in patterns:
        for match in pattern.finditer(response):
            title = match.group(1).strip().lower()
            words = title.split()
            # Skip sentence starters and single-word matches (too ambiguous)
            if not words or words[0] in _TITLE_SENTENCE_STARTERS:
                continue
            if len(words) < 2:
                continue
            titles.add(title)
    return {title for title in titles if title}


def _extract_claimed_course_titles(response: str) -> set[str]:
    titles: set[str] = set()
    trailing_stop = {"next", "first", "instead", "afterward", "afterwards", "now", "later"}
    patterns = [
        re.compile(
            rf"(?i:\b(?:take|recommend|recommended|enroll in|consider))\s+({TITLE_WORD_PATTERN})",
        ),
        re.compile(
            rf"(?i:\b(?:course|class))\s+({TITLE_WORD_PATTERN})",
        ),
        re.compile(
            rf"\b({TITLE_WORD_PATTERN})\s+(?:would help|could help|may help|is relevant|is useful|is a good option)\b",
        ),
        re.compile(
            rf"(?i:\b(?:like|such as))\s+({TITLE_WORD_PATTERN})",
        ),
    ]
    for pattern in patterns:
        for match in pattern.finditer(response):
            words = match.group(1).strip().rstrip(".,;:").split()
            while words and words[-1].lower() in trailing_stop:
                words.pop()
            if not words:
                continue
            title = " ".join(words).lower()
            # Must be at least 2 meaningful words and not a bare skill/language token
            if len(words) < 2:
                continue
            if title in _SKILL_TOKENS_NOT_COURSE_TITLES:
                continue
            # Skip if the whole title is just a skill token with noise
            if len(title) < 8:
                continue
            titles.add(title)
    return {title for title in titles if title}


def _bundle_gap_skills(bundle: dict) -> set[str]:
    return {
        normalize_skill_name(skill)
        for job in bundle.get("jobs", [])
        for skill in job.get("gaps", [])
        if skill
    }


def _bundle_course_support(bundle: dict) -> dict[str, set[str]]:
    course_support: dict[str, set[str]] = {}
    for course in bundle.get("courses", []):
        code = (course.get("course_code") or "").strip().upper()
        if not code:
            continue
        supported = {
            normalize_skill_name(skill)
            for skill in (course.get("teaches", []) or []) + (course.get("addresses_gaps", []) or [])
            if skill
        }
        course_support[code] = supported
    return course_support


def _question_terms(question: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9+#.]+", (question or "").lower())
        if len(token) >= 4
    }


def _fallback_relevance_score(question: str, response: str) -> int:
    q_terms = _question_terms(question)
    if not q_terms:
        return 6 if response.strip() else 0
    response_terms = _question_terms(response)
    overlap = len(q_terms & response_terms)
    if overlap >= 4:
        return 8
    if overlap >= 2:
        return 7
    if overlap >= 1:
        return 6
    return 4 if response.strip() else 0


def _fallback_utility_score(bundle: dict, response: str) -> int:
    response_upper = response.upper()
    course_codes = {
        (course.get("course_code") or "").strip().upper()
        for course in bundle.get("courses", [])
        if course.get("course_code")
    }
    mentions_course = any(code and code in response_upper for code in course_codes)
    mentions_gaps = bool(re.search(r"\b(gap|gaps|missing|next step|learn|build)\b", response, re.IGNORECASE))
    if mentions_course and mentions_gaps:
        return 8
    if mentions_course or mentions_gaps:
        return 7
    return 5 if response.strip() else 0


def _extract_claimed_skills(response: str) -> set[str]:
    claims: set[str] = set()

    cue_patterns = [
        r"learn\s+([A-Za-z0-9+#./-]+(?:\s+[A-Za-z0-9+#./-]+)?)",
        r"missing\s+([A-Za-z0-9+#./-]+(?:\s+[A-Za-z0-9+#./-]+)?)",
        r"gap(?:s)?\s+(?:is|are)\s+([A-Za-z0-9+#./-]+(?:\s+[A-Za-z0-9+#./-]+)?)",
    ]
    for pattern in cue_patterns:
        for match in re.finditer(pattern, response, re.IGNORECASE):
            raw = normalize_skill_name(match.group(1))
            # Skip stop words and overly long strings (sentences, not skills)
            if raw in _SKILL_STOP_WORDS or len(raw.split()) > 4 or len(raw) > 40:
                continue
            claims.add(raw)

    for match in re.finditer(r"skills?:\s*([A-Za-z0-9+#./,\-\s]+)", response, re.IGNORECASE):
        for raw_part in match.group(1).split(","):
            part = raw_part.strip()
            if not part:
                continue
            normalized = normalize_skill_name(part)
            if normalized in _SKILL_STOP_WORDS or len(normalized.split()) > 4 or len(normalized) > 40:
                continue
            claims.add(normalized)

    return {claim for claim in claims if claim}


def _validate_citations(citations: list[dict], entities: dict[str, set[str]]) -> list[str]:
    """Check that each LLM-generated citation source can be traced to the evidence bundle."""
    violations: list[str] = []
    all_allowed = (
        entities["job_titles"]
        | entities["course_titles"]
        | {c.lower() for c in entities["course_codes"]}
        | entities["skills"]
        | entities["companies"]
    )
    for item in citations or []:
        source = (item.get("source") or "").strip().lower()
        if not source:
            continue
        # Skip generic meta-references — the LLM cited the prompt structure, not actual evidence
        if any(source.startswith(prefix) for prefix in _CITATION_META_PREFIXES):
            continue
        # Fuzzy match: source contains an allowed entity OR an allowed entity contains the source
        if any(source == allowed or allowed in source or source in allowed for allowed in all_allowed):
            continue
        violations.append(f"citation source {source!r} not found in evidence")
    return violations[:3]


def _deterministic_support_checks(bundle: dict, response: str) -> tuple[int, list[str]]:
    entities = _allowed_entities(bundle)
    gap_skills = _bundle_gap_skills(bundle)
    course_support = _bundle_course_support(bundle)
    penalties: list[str] = []
    response_lower = response.lower()

    mentioned_course_codes = set(re.findall(r"\b[A-Z]{2,4}\s*\d{3}\b", response.upper()))
    unsupported_courses = sorted(code for code in mentioned_course_codes if code not in entities["course_codes"])
    if unsupported_courses:
        penalties.append(f"unsupported course codes: {', '.join(unsupported_courses[:3])}")

    mentioned_job_titles = _extract_claimed_job_titles(response)
    unsupported_job_titles = sorted(
        title for title in mentioned_job_titles
        if title not in entities["job_titles"]
    )
    if unsupported_job_titles:
        penalties.append(f"unsupported job titles: {', '.join(unsupported_job_titles[:2])}")

    mentioned_course_titles = _extract_claimed_course_titles(response)
    unsupported_course_titles = sorted(
        title for title in mentioned_course_titles
        if title not in entities["course_titles"]
    )
    if unsupported_course_titles:
        penalties.append(f"unsupported course titles: {', '.join(unsupported_course_titles[:2])}")

    mentioned_companies = {
        company for company in entities["companies"]
        if company and re.search(rf"\b{re.escape(company)}\b", response_lower)
    }
    if COMPANY_REFERENCE_PATTERN.search(response) and not mentioned_companies and entities["companies"]:
        penalties.append("company references do not align with retrieved jobs")

    quoted_skills = _extract_claimed_skills(response)
    unsupported_skills = sorted(
        skill for skill in quoted_skills
        if skill and skill not in entities["skills"]
    )
    if unsupported_skills:
        penalties.append(f"unsupported skill mentions: {', '.join(unsupported_skills[:3])}")

    if "[insert" in response_lower or "placeholder" in response_lower:
        penalties.append("response contains placeholder text")

    if "we can infer" in response_lower or "speculative" in response_lower:
        penalties.append("response makes speculative claims beyond retrieved evidence")

    if any(phrase in response_lower for phrase in ["online resource", "outside course", "elective course", "you could also take", "alternatively, you could"]):
        penalties.append("response suggests non-retrieved learning resources")

    if any(phrase in response_lower for phrase in ["not required", "neither of the job postings require", "does not require this skill"]):
        penalties.append("response contradicts retrieved job requirements")

    if course_support and gap_skills:
        # Only check gap-support when we have actual gaps to verify against.
        # A course with an empty teaches list or one not in the bundle is caught
        # by the unsupported-course-codes check above.
        course_mentions = list(re.finditer(r"\b([A-Z]{2,4}\s*\d{3})\b", response.upper()))
        for match in course_mentions:
            code = match.group(1).strip().upper()
            if code not in course_support:
                # Already flagged as unsupported code above — skip here
                continue
            supported_skills = course_support[code]
            if not supported_skills:
                # Course has no teaches data; give benefit of the doubt
                continue
            if not (supported_skills & gap_skills):
                # Course teaches nothing that is in the gap list
                penalties.append(f"course recommendation lacks gap support for {code}")
                break
            window_start = max(0, match.start() - 140)
            window_end = min(len(response), match.end() + 220)
            window = response[window_start:window_end]
            claimed_window_skills = _extract_claimed_skills(window)
            unsupported_for_course = sorted(
                skill for skill in claimed_window_skills
                if skill in gap_skills and skill not in supported_skills
            )
            if unsupported_for_course:
                penalties.append(
                    f"course recommendation overclaims support for {code}: {', '.join(unsupported_for_course[:2])}"
                )
                break

    support_score = 10 - min(6, len(penalties) * 2)
    if not bundle.get("jobs") and not bundle.get("courses") and len(response.split()) > 50:
        penalties.append("answer is overly specific despite empty evidence")
        support_score = min(support_score, 4)
    return max(0, support_score), penalties


def _parse_critique_json(raw: str) -> dict:
    """Multi-strategy JSON extraction for deepseek-r1 output."""
    # Strategy 1: direct parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Strategy 2: find outermost {...} block
    brace_match = re.search(r"\{.*\}", raw, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    # Strategy 3: extract individual fields with regex
    result: dict = {}
    for field in ("relevance", "support", "utility"):
        m = re.search(rf'["\']?{field}["\']?\s*:\s*(\d+)', raw, re.IGNORECASE)
        if m:
            result[field] = int(m.group(1))
    critique_match = re.search(
        r'["\']?critique["\']?\s*:\s*["\']([^"\']+)["\']', raw, re.IGNORECASE
    )
    if critique_match:
        result["critique"] = critique_match.group(1).strip()

    if {"relevance", "support", "utility"}.issubset(result):
        result.setdefault("critique", "")
        result.setdefault("evidence_citations", [])
        return result

    raise ValueError(f"Cannot parse critique JSON from: {raw[:200]!r}")


def _llm_scores_with_details(question: str, context: str, response: str, bundle: dict | None = None) -> dict:
    prompt = CRITIQUE_PROMPT.format(
        question=question,
        context=context[:4000],
        response=response[:1800],
    )
    resp = httpx.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": CRITIQUE_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=60,
    )
    resp.raise_for_status()
    payload = resp.json()
    raw = payload["message"]["content"].strip()

    # Strip deepseek-r1 <think>...</think> reasoning block
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    # Strip markdown code fences
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:].strip()

    scores = _parse_critique_json(raw)
    scores = {k.strip().strip('"').strip("'"): v for k, v in scores.items()}

    citation_violations: list[str] = []
    if bundle is not None:
        entities = _allowed_entities(bundle)
        citation_violations = _validate_citations(scores.get("evidence_citations", []), entities)

    parsed_scores = {
        "relevance": max(0, min(10, int(scores.get("relevance", 5)))),
        "support": max(0, min(10, int(scores.get("support", 5)))),
        "utility": max(0, min(10, int(scores.get("utility", 5)))),
        "critique": str(scores.get("critique", "")).strip(),
        "citation_violations": citation_violations,
    }
    return {
        "scores": parsed_scores,
        "usage_metadata": ollama_usage_metadata(payload),
        "timing_metadata": ollama_timing_metadata(payload),
        "raw_response": raw,
    }


def critique_candidate_details(question: str, bundle: dict, context: str, response: str) -> dict:
    """
    Returns: { "relevance": int, "support": int, "utility": int,
               "critique": str, "total": float, "support_findings": list[str] }
    """
    deterministic_support, findings = _deterministic_support_checks(bundle, response)
    usage_metadata = None
    timing_metadata = None
    raw_response = None

    try:
        llm_result = _llm_scores_with_details(question, context, response, bundle=bundle)
        llm_scores = llm_result["scores"]
        usage_metadata = llm_result["usage_metadata"]
        timing_metadata = llm_result["timing_metadata"]
        raw_response = llm_result["raw_response"]
        relevance = llm_scores["relevance"]
        utility = llm_scores["utility"]
        support = min(llm_scores["support"], deterministic_support)
        critique = llm_scores["critique"]
        findings.extend(llm_scores.get("citation_violations", []))
    except Exception:
        relevance = _fallback_relevance_score(question, response)
        utility = _fallback_utility_score(bundle, response)
        support = deterministic_support
        critique = "fallback critique"

    if findings:
        critique = "; ".join(findings[:2]) if not critique else f"{critique} | {'; '.join(findings[:2])}"

    # Weights: relevance 35% · support 40% · utility 25%
    # Old formula (support 50%, utility 30%, relevance 20%) allowed a completely
    # irrelevant but well-supported answer to score 8.0. Relevance is now a
    # meaningful gate — a zero-relevance response can score at most 6.5.
    total = round(relevance * 0.35 + support * 0.40 + utility * 0.25, 2)
    scores = {
        "relevance": relevance,
        "support": support,
        "utility": utility,
        "critique": critique,
        "support_findings": findings,
        "total": total,
    }
    return {
        "scores": scores,
        "usage_metadata": usage_metadata,
        "timing_metadata": timing_metadata,
        "raw_response": raw_response,
    }


def critique_candidate(question: str, bundle: dict, context: str, response: str) -> dict:
    return critique_candidate_details(question, bundle, context, response)["scores"]
