import src.core.env as env

from functools import lru_cache
from google import genai
from google.genai import types

@lru_cache(maxsize=1)
def get_gemini_client():
    gemini_client = genai.Client(
        api_key=env.GEMINI_API_KEY,
        http_options=types.HttpOptions(timeout=120_000)
    )

    return gemini_client

