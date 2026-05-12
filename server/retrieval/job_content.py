import re
from collections.abc import Iterable

from retrieval.record_utils import job_skills_value
from retrieval.skills import normalize_skill_name


SKILL_PATTERNS: dict[str, tuple[str, ...]] = {
    # Languages
    "Python": (r"\bpython\b",),
    "Java": (r"\bjava\b",),
    "JavaScript": (r"\bjavascript\b",),
    "TypeScript": (r"\btypescript\b",),
    "C++": (r"\bc\+\+\b", r"\bcpp\b"),
    "C#": (r"\bc#\b", r"\bc sharp\b"),
    "C": (r"\blanguage c\b", r"\bwritten in c\b", r"\bc programming\b"),
    "Go": (r"\bgolang\b", r"\b(?:in|using) go\b"),
    "Rust": (r"\brust\b",),
    "Scala": (r"\bscala\b",),
    "Kotlin": (r"\bkotlin\b",),
    "Swift": (r"\bswift\b",),
    "R": (r"\bR programming\b", r"\blanguage R\b", r"\bin R\b"),
    "Julia": (r"\bjulia\b",),
    "MATLAB": (r"\bmatlab\b",),
    # Web / Frontend
    "React": (r"\breact(?:\.js)?\b",),
    "Next.js": (r"\bnext(?:\.js)?\b",),
    "Vue.js": (r"\bvue(?:\.js)?\b",),
    "Angular": (r"\bangular\b",),
    "HTML/CSS": (r"\bhtml\b", r"\bcss\b"),
    "GraphQL": (r"\bgraphql\b",),
    "REST APIs": (r"\brest(?:ful)? api\b",),
    "gRPC": (r"\bgrpc\b",),
    # Backend / Frameworks
    "Node.js": (r"\bnode(?:\.js)?\b",),
    "Django": (r"\bdjango\b",),
    "FastAPI": (r"\bfastapi\b",),
    "Flask": (r"\bflask\b",),
    "Spring Boot": (r"\bspring boot\b",),
    # Databases
    "SQL": (r"\bsql\b",),
    "PostgreSQL": (r"\bpostgres(?:ql)?\b",),
    "MySQL": (r"\bmysql\b",),
    "MongoDB": (r"\bmongodb\b",),
    "Redis": (r"\bredis\b",),
    "Elasticsearch": (r"\belasticsearch\b",),
    "Cassandra": (r"\bcassandra\b",),
    "DynamoDB": (r"\bdynamodb\b",),
    "Snowflake": (r"\bsnowflake\b",),
    "BigQuery": (r"\bbigquery\b",),
    # Cloud & Infra
    "AWS": (r"\baws\b", r"\bamazon web services\b"),
    "GCP": (r"\bgcp\b", r"\bgoogle cloud\b"),
    "Azure": (r"\bazure\b",),
    "Docker": (r"\bdocker\b",),
    "Kubernetes": (r"\bkubernetes\b", r"\bk8s\b"),
    "Terraform": (r"\bterraform\b",),
    "CI/CD": (r"\bci/cd\b", r"\bcontinuous integration\b", r"\bcontinuous delivery\b"),
    "GitHub Actions": (r"\bgithub actions\b",),
    "Kafka": (r"\bkafka\b",),
    "Airflow": (r"\bairflow\b",),
    "Spark": (r"\bapache spark\b", r"\bpyspark\b", r"\bspark\b"),
    "Linux": (r"\blinux\b", r"\bunix\b"),
    "Git": (r"\bgit\b",),
    # ML / AI
    "Machine Learning": (r"\bmachine learning\b",),
    "Deep Learning": (r"\bdeep learning\b",),
    "PyTorch": (r"\bpytorch\b",),
    "TensorFlow": (r"\btensorflow\b",),
    "Scikit-learn": (r"\bscikit-learn\b", r"\bsklearn\b"),
    "Hugging Face Transformers": (r"\bhugging face\b", r"\btransformers\b"),
    "LLMs": (r"\bllm(?:s)?\b", r"\blarge language model\b"),
    "Retrieval-Augmented Generation": (r"\brag\b", r"\bretrieval.augmented generation\b"),
    "Prompt Engineering": (r"\bprompt engineering\b",),
    "Natural Language Processing": (r"\bnlp\b", r"\bnatural language processing\b"),
    "Computer Vision": (r"\bcomputer vision\b",),
    "Reinforcement Learning": (r"\breinforcement learning\b",),
    "MLOps": (r"\bmlops\b", r"\bml ops\b"),
    "Feature Engineering": (r"\bfeature engineering\b",),
    "A/B Testing": (r"\ba/b testing\b", r"\bexperimentation\b"),
    "Statistical Modeling": (r"\bstatistical model\b", r"\bstatistics\b"),
    # Data & Analytics
    "Pandas": (r"\bpandas\b",),
    "NumPy": (r"\bnumpy\b",),
    "Data Pipelines": (r"\bdata pipeline\b", r"\betl\b", r"\belt\b"),
    "Data Visualization": (r"\bdata visualization\b", r"\btableau\b", r"\bpower bi\b"),
    "Jupyter Notebooks": (r"\bjupyter\b",),
    # Systems
    "Distributed Systems": (r"\bdistributed systems?\b",),
    "Microservices": (r"\bmicroservice\b",),
    "System Design": (r"\bsystem design\b",),
    "Data Structures": (r"\bdata structures?\b",),
    "Algorithms": (r"\balgorithms?\b",),
    "Operating Systems": (r"\boperating systems?\b",),
    # Security
    "Cybersecurity": (r"\bcybersecurity\b", r"\bsecurity\b"),
    "Cryptography": (r"\bcryptography\b",),
    # Mobile
    "iOS Development": (r"\bios development\b", r"\bswiftui\b", r"\buikit\b"),
    "Android Development": (r"\bandroid\b", r"\bjetpack compose\b"),
    "React Native": (r"\breact native\b",),
    "Flutter": (r"\bflutter\b",),
    # SE practices
    "Testing": (r"\bunit test\b", r"\bintegration test\b", r"\bpytest\b", r"\bjunit\b"),
    "Agile/Scrum": (r"\bagile\b", r"\bscrum\b",),
    "Code Review": (r"\bcode review\b",),
    "Technical Communication": (r"\btechnical communication\b", r"\bdocumentation\b"),
}


def extract_job_skills(title: str, description: str, precomputed: str = "") -> list[str]:
    """Return skills for a job.

    If *precomputed* is a non-empty pipe-delimited string (from the CSV's
    ai_key_skills column), return those directly.  Otherwise fall back to
    pattern-matching against the title + description.
    """
    if precomputed:
        skills = [s.strip() for s in precomputed.split("|") if s.strip()]
        if skills:
            return skills

    text = " ".join(part for part in [title, description] if part).lower()
    found: list[str] = []
    seen: set[str] = set()

    for skill, patterns in SKILL_PATTERNS.items():
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
            normalized = normalize_skill_name(skill)
            if normalized not in seen:
                found.append(skill)
                seen.add(normalized)
    return found


def build_job_embedding_text(job: dict) -> str:
    skills = job_skills_value(job)
    sections = [
        f"Job Title: {job.get('title', '').strip()}",
        f"Company: {job.get('company', '').strip()}",
    ]
    if job.get("location"):
        sections.append(f"Location: {job.get('location', '').strip()}")
    if skills:
        sections.append(f"Skills: {', '.join(skills)}")
    if job.get("description"):
        sections.append(f"Description:\n{job.get('description', '').strip()}")
    return "\n".join(section for section in sections if section.strip())


def chunk_text(text: str, max_chars: int = 1400, overlap: int = 200) -> list[str]:
    compact = re.sub(r"\s+", " ", (text or "").strip())
    if not compact:
        return []
    if len(compact) <= max_chars:
        return [compact]

    words = compact.split(" ")
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for word in words:
        projected = current_len + len(word) + (1 if current else 0)
        if current and projected > max_chars:
            chunk = " ".join(current)
            chunks.append(chunk)
            if overlap > 0:
                overlap_words: list[str] = []
                overlap_len = 0
                for existing in reversed(current):
                    additional = len(existing) + (1 if overlap_words else 0)
                    if overlap_len + additional > overlap:
                        break
                    overlap_words.insert(0, existing)
                    overlap_len += additional
                current = overlap_words
                current_len = len(" ".join(current))
            else:
                current = []
                current_len = 0

        current.append(word)
        current_len = current_len + len(word) + (1 if len(current) > 1 else 0)

    if current:
        chunks.append(" ".join(current))
    return chunks


def average_vectors(vectors: Iterable[list[float]]) -> list[float]:
    vector_list = [vector for vector in vectors if vector]
    if not vector_list:
        return []
    dimensions = len(vector_list[0])
    totals = [0.0] * dimensions
    for vector in vector_list:
        if len(vector) != dimensions:
            raise ValueError("Cannot average vectors with different dimensions.")
        for index, value in enumerate(vector):
            totals[index] += value
    count = float(len(vector_list))
    return [value / count for value in totals]
