from functools import lru_cache
from typing import Any

from google import genai
from google.genai import types

from app.config import GEMINI_EMBEDDING_MODEL, GOOGLE_API_KEY


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not set. Create backend/.env from .env.example.")
    return genai.Client(api_key=GOOGLE_API_KEY)


async def generate_embedding_from_text(
    text: str,
    task_type: str = "RETRIEVAL_QUERY",
) -> list[float]:
    return await _embed(text, task_type=task_type)


async def _embed(text: str, task_type: str) -> list[float]:
    response = await _client().aio.models.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return _extract_embedding(response)


def _extract_embedding(response: Any) -> list[float]:
    embeddings = getattr(response, "embeddings", None)
    if embeddings:
        first_embedding = embeddings[0]
        values = getattr(first_embedding, "values", None)
        if values is not None:
            return list(values)

    embedding = getattr(response, "embedding", None)
    if embedding is not None:
        values = getattr(embedding, "values", embedding)
        return list(values)

    if isinstance(response, dict):
        if "embedding" in response and response["embedding"] is not None:
            return list(response["embedding"])
        if "embeddings" in response and response["embeddings"]:
            first_embedding = response["embeddings"][0]
            if isinstance(first_embedding, dict) and "values" in first_embedding:
                return list(first_embedding["values"])

    raise ValueError("Gemini did not return an embedding.")
