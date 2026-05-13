import os
from functools import lru_cache

from dotenv import load_dotenv

from retrieval.job_content import average_vectors, chunk_text
from retrieval.providers import embed_text as _provider_embed

load_dotenv()


@lru_cache(maxsize=1024)
def _embed_cached(text: str) -> tuple[float, ...]:
    """Cached embedding call routed through the active provider."""
    return tuple(_provider_embed(text))


def embed(text: str) -> list[float]:
    return list(_embed_cached(text))


def embed_batch(texts: list[str]) -> list[list[float]]:
    return [embed(t) for t in texts]


def embed_long_text(text: str, max_chars: int = 1400, overlap: int = 200) -> list[float]:
    chunks = chunk_text(text, max_chars=max_chars, overlap=overlap)
    if not chunks:
        return embed("")
    if len(chunks) == 1:
        return embed(chunks[0])
    return average_vectors(embed_batch(chunks))
