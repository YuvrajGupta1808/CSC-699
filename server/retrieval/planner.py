import json
import re

from langsmith import traceable

from retrieval.prompts import CLASSIFY_PROMPT
from retrieval.providers import chat_complete as provider_chat_complete, planner_model

GREETING_KEYWORDS = {"hi", "hello", "hey", "thanks", "thank you"}
JOB_KEYWORDS = {"job", "jobs", "role", "roles", "position", "positions", "intern", "internship", "career", "hiring"}
COURSE_KEYWORDS = {"course", "courses", "class", "classes", "learn", "learning", "upskill", "study", "take"}
BROAD_ANALYSIS_KEYWORDS = {"roadmap", "plan", "path", "readiness", "prepare", "qualified", "career path"}
SKILL_GAP_PHRASES = {"skill gap", "skill gaps", "missing skills", "close gaps", "close my gaps"}
FOLLOWUP_REFERENCE_WORDS = {"those", "them", "that", "it", "they", "which", "these", "there", "this", "any", "do", "does"}

_REQUIRED_INTENT_KEYS = {"intent", "top_k_jobs", "top_k_courses"}
_VALID_INTENTS = {"greeting", "jobs", "skill_gap", "courses", "broad", "general"}
_DEFAULT_INTENT_REASON = {
    "greeting":   "small talk or no career question detected",
    "jobs":       "job-fit or role recommendation question",
    "skill_gap":  "skill-gap question requires job context",
    "courses":    "learning or upskill question",
    "broad":      "broad readiness or roadmap question",
    "general":    "general advisory question",
}


def _llm_classify_intent(question: str, history_summary: str) -> dict | None:
    prompt = CLASSIFY_PROMPT.format(question=question, history_summary=history_summary)
    try:
        raw = provider_chat_complete(
            [{"role": "user", "content": prompt}],
            model_role="planner",
            timeout=10,
            temperature=0.0,
        )
        raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw)
        result = {k.strip().strip('"').strip("'"): v for k, v in result.items()}
        if not _REQUIRED_INTENT_KEYS.issubset(result.keys()):
            return None
        if result.get("intent") not in _VALID_INTENTS:
            return None
        result["top_k_jobs"] = max(0, int(result["top_k_jobs"]))
        result["top_k_courses"] = max(0, int(result["top_k_courses"]))
        reason = result.get("reason") or result.get("reasoning") or ""
        result["reason"] = reason.strip() or _DEFAULT_INTENT_REASON.get(result["intent"], "llm classified")
        return result
    except Exception:
        return None


def _contains_term(tokens: list[str], terms: set[str]) -> bool:
    token_set = set(tokens)
    for term in terms:
        term_tokens = re.findall(r"[a-z0-9+#.]+", term.lower())
        if not term_tokens:
            continue
        if len(term_tokens) == 1:
            if term_tokens[0] in token_set:
                return True
            continue
        window = len(term_tokens)
        for index in range(len(tokens) - window + 1):
            if tokens[index:index + window] == term_tokens:
                return True
    return False


def _infer_intent_from_history(history: list[dict]) -> str | None:
    """Return the dominant topic from the last few conversation turns."""
    for turn in reversed(history[-4:]):
        content = turn.get("content", "").lower()
        turn_tokens = set(re.findall(r"[a-z0-9+#.]+", content))
        if turn_tokens & JOB_KEYWORDS:
            return "jobs"
        if turn_tokens & COURSE_KEYWORDS:
            return "courses"
    return None


def _keyword_classify(question: str, conversation_history: list[dict] | None) -> dict:
    """Keyword-based fallback classifier."""
    q = question.lower()
    compact = " ".join(q.split())

    if not compact or all(not c.isalnum() for c in compact):
        return {"intent": "greeting", "top_k_jobs": 0, "top_k_courses": 0, "reason": "empty or non-alphanumeric input"}

    if compact in GREETING_KEYWORDS or len(compact.split()) <= 2 and compact in GREETING_KEYWORDS:
        return {"intent": "greeting", "top_k_jobs": 0, "top_k_courses": 0, "reason": "greeting or small talk"}

    token_list = re.findall(r"[a-z0-9+#.]+", compact)
    tokens = set(token_list)

    asks_for_jobs = bool(tokens & JOB_KEYWORDS)
    asks_for_courses = bool(tokens & COURSE_KEYWORDS)
    asks_for_broad_analysis = _contains_term(token_list, BROAD_ANALYSIS_KEYWORDS)
    mentions_skill_gap = _contains_term(token_list, SKILL_GAP_PHRASES)
    asks_what_skills_for_roles = ("skills" in tokens or "skill" in tokens) and asks_for_jobs
    asks_for_course_recommendations = asks_for_courses or mentions_skill_gap

    has_domain_signal = asks_for_jobs or asks_for_courses or asks_for_broad_analysis or mentions_skill_gap
    is_short = len(token_list) <= 8
    has_reference = bool(tokens & FOLLOWUP_REFERENCE_WORDS)
    if is_short and has_reference and not has_domain_signal and conversation_history:
        prior_intent = _infer_intent_from_history(conversation_history)
        if prior_intent == "jobs":
            return {"intent": "jobs", "top_k_jobs": 5, "top_k_courses": 1, "reason": "follow-up on job discussion"}
        if prior_intent == "courses":
            return {"intent": "courses", "top_k_jobs": 0, "top_k_courses": 5, "reason": "follow-up on course discussion"}

    if asks_for_broad_analysis or (asks_for_jobs and asks_for_course_recommendations):
        return {"intent": "broad", "top_k_jobs": 6, "top_k_courses": 6, "reason": "broad readiness analysis"}
    if asks_what_skills_for_roles and not asks_for_course_recommendations:
        return {"intent": "jobs", "top_k_jobs": 6, "top_k_courses": 2, "reason": "job-oriented skill requirements question"}
    if asks_for_course_recommendations:
        # Skill-gap questions need job context to define the gap
        if mentions_skill_gap:
            return {"intent": "skill_gap", "top_k_jobs": 3, "top_k_courses": 6, "reason": "skill-gap question requires job context"}
        return {"intent": "courses", "top_k_jobs": 0, "top_k_courses": 6, "reason": "learning and skill-gap question"}
    if asks_for_jobs:
        return {"intent": "jobs", "top_k_jobs": 6, "top_k_courses": 2, "reason": "job-fit or recommendation question"}
    return {"intent": "general", "top_k_jobs": 3, "top_k_courses": 3, "reason": "general advisory question"}


@traceable(name="plan_retrieval", run_type="chain")
def plan_retrieval(question: str, conversation_history: list[dict] | None = None) -> dict:
    history = conversation_history or []
    history_summary = " / ".join(
        f"{t.get('role', 'user').capitalize()}: {(t.get('content') or '')[:120]}"
        for t in history[-2:]
    ) or "none"

    llm_result = _llm_classify_intent(question, history_summary)
    if llm_result is not None:
        # Enforce invariant: skill_gap always retrieves job context
        if llm_result.get("intent") == "skill_gap":
            llm_result["top_k_jobs"] = max(3, llm_result["top_k_jobs"])
        llm_result["classifier"] = "llm"
        return llm_result

    result = _keyword_classify(question, history)
    # Enforce invariant: skill_gap always retrieves job context
    if result.get("intent") == "skill_gap":
        result["top_k_jobs"] = max(3, result["top_k_jobs"])
    result["classifier"] = "keyword_fallback"
    return result
