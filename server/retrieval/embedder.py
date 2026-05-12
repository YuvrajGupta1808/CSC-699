import os
from functools import lru_cache

import httpx
from dotenv import load_dotenv

from retrieval.job_content import average_vectors, chunk_text

load_dotenv()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")


@lru_cache(maxsize=1024)
def _embed_cached(text: str) -> tuple[float, ...]:
    """Cached Ollama embedding call. Returns a tuple so it is hashable/cacheable."""
    response = httpx.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=30,
    )
    response.raise_for_status()
    return tuple(response.json()["embedding"])


def embed(text: str) -> list[float]:
    """Return a cached embedding vector for text."""
    return list(_embed_cached(text))


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts, hitting the cache for any repeated strings."""
    return [embed(t) for t in texts]


def embed_long_text(text: str, max_chars: int = 1400, overlap: int = 200) -> list[float]:
    """Embed longer text by averaging overlapping chunk embeddings."""
    chunks = chunk_text(text, max_chars=max_chars, overlap=overlap)
    if not chunks:
        return embed("")
    if len(chunks) == 1:
        return embed(chunks[0])
    return average_vectors(embed_batch(chunks))
