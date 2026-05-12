import re

from retrieval.skills import normalize_skill_name


def query_terms(text: str) -> set[str]:
    raw_tokens = re.findall(r"[a-z0-9+#.]+", (text or "").lower())
    result: set[str] = set()
    for token in raw_tokens:
        if len(token) >= 3:
            result.add(token)
            normalized = normalize_skill_name(token)
            if normalized and normalized != token:
                result.add(normalized)
    return result
