from app.config import GEMINI_CHAT_MODEL
from app.utils.embeddings import _client


async def generate_response(prompt: str) -> str:
    # TODO: Add retry and resilience handling here, including exponential backoff for rate limits and transient API errors.
    response = await _client().aio.models.generate_content(
        model=GEMINI_CHAT_MODEL,
        contents=prompt,
    )
    if not response.text:
        raise ValueError("Gemini did not return any text.")
    return response.text.strip()
