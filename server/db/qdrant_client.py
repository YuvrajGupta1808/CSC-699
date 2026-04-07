import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

_client: QdrantClient | None = None


def get_qdrant() -> QdrantClient:
    global _client
    if _client is None:
        url = os.environ.get("QDRANT_URL", "http://localhost:6333")
        _client = QdrantClient(url=url)
    return _client
