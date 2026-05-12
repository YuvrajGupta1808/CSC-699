import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_client: Any | None = None


def get_supabase():
    global _client
    if _client is None:
        from supabase import create_client

        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_KEY"]
        _client = create_client(url, key)
    return _client
