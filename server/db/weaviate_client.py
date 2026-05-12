import os

import weaviate
from dotenv import load_dotenv

load_dotenv()

_client: weaviate.WeaviateClient | None = None


def get_weaviate() -> weaviate.WeaviateClient:
    global _client
    if _client is None or not _client.is_connected():
        url = os.environ.get("WEAVIATE_URL", "http://localhost:8080")
        # Strip scheme; connect_to_local takes host + port separately
        host_port = url.removeprefix("http://").removeprefix("https://")
        host, _, port_str = host_port.partition(":")
        port = int(port_str) if port_str else 8080
        _client = weaviate.connect_to_local(host=host, port=port, grpc_port=50051)
    return _client
