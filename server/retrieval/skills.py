import re


SKILL_ALIAS_MAP = {
    # abbreviations
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "js": "javascript",
    "ts": "typescript",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "oop": "object-oriented programming",
    "dsa": "data structures",
    "db": "databases",
    "os": "operating systems",
    # dot-notation variants
    "node.js": "nodejs",
    "node js": "nodejs",
    "vue.js": "vuejs",
    "vue js": "vuejs",
    "react.js": "react",
    "react js": "react",
    "next.js": "nextjs",
    "next js": "nextjs",
    "express.js": "expressjs",
    "express js": "expressjs",
    # "X API" → "X" (REST API, GraphQL API, etc.)
    "rest api": "rest",
    "restful api": "rest",
    "restful apis": "rest",
    "rest apis": "rest",
    "graphql api": "graphql",
    "grpc api": "grpc",
    # Cloud service suffixes — match product to platform
    "aws s3": "aws",
    "aws lambda": "aws",
    "aws ec2": "aws",
    "aws rds": "aws",
    "aws ecs": "aws",
    "aws eks": "aws",
    "gcp gke": "gcp",
    "google cloud": "gcp",
    "azure devops": "azure",
    # CI/CD variants
    "ci cd": "ci/cd",
    "cicd": "ci/cd",
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",
    # language aliases
    "c plus plus": "c++",
    "golang": "go",
    "rust lang": "rust",
    "kotlin android": "kotlin",
}

# Strip trailing version strings BEFORE dot/slash normalization, e.g. "2.0", "v3", "2.x"
_VERSION_SUFFIX_RAW = re.compile(r"\s+v?\d[\d.x]*$")
# Strip trailing purely-numeric tokens after dot normalization, e.g. "tensorflow 2 0"
_TRAILING_DIGITS = re.compile(r"(\s+\d+)+$")


def normalize_skill_name(value: str) -> str:
    text = (value or "").strip().lower()
    # Strip version suffix while dots are still intact ("2.0" not yet split)
    text = _VERSION_SUFFIX_RAW.sub("", text).strip()
    text = text.replace("&", " and ")
    text = re.sub(r"[/_,.-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    # Catch any residual trailing digit tokens (e.g. "tensorflow 2 0" → "tensorflow")
    text = _TRAILING_DIGITS.sub("", text).strip()
    return SKILL_ALIAS_MAP.get(text, text)


def extract_skill_names(skills_array) -> list[str]:
    """
    Normalize skills field — handles both:
      [{"skill": "Python", "weight": 40}, ...]   (jobs format)
      [["Python", 40], ...]                       (courses format)
      ["Python", ...]                             (plain list)
    """
    if not skills_array:
        return []
    names = []
    for item in skills_array:
        if isinstance(item, dict):
            names.append(item.get("skill") or item.get("name") or "")
        elif isinstance(item, (list, tuple)) and len(item) >= 1:
            names.append(str(item[0]))
        elif isinstance(item, str):
            names.append(item)
    return [n.strip() for n in names if n and n.strip()]


def build_skill_index(skills: list[str]) -> dict[str, str]:
    """
    Returns normalized -> canonical skill name using first-seen canonical casing.
    """
    index: dict[str, str] = {}
    for skill in skills or []:
        normalized = normalize_skill_name(skill)
        if normalized and normalized not in index:
            index[normalized] = skill.strip()
    return index


def normalized_skill_set(skills: list[str]) -> set[str]:
    return {normalize_skill_name(skill) for skill in skills or [] if normalize_skill_name(skill)}


def count_skill_overlap(left: list[str], right: list[str]) -> int:
    return len(normalized_skill_set(left) & normalized_skill_set(right))


def skills_overlap(left: list[str], right: list[str]) -> bool:
    return count_skill_overlap(left, right) > 0


def compute_skill_overlap(required_skills: list[str], student_skills: list[str]) -> tuple[list[str], list[str]]:
    student_index = build_skill_index(student_skills)
    covered: list[str] = []
    gaps: list[str] = []
    for skill in required_skills:
        normalized = normalize_skill_name(skill)
        if normalized in student_index:
            covered.append(skill)
        else:
            gaps.append(skill)
    return covered, gaps
