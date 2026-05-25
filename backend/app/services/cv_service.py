from typing import Any

from app.schemas.search import SearchRequest
from app.utils.embeddings import generate_embedding_from_text
from app.utils.llm import generate_response
from app.utils.prompts import build_prompt, build_question_rewrite_prompt
from app.storage.vector_store import get_cvs_similar_to_embedding

CV_SEARCH_LIMIT = 10

async def _rewrite_question(
    question: str,
    history: list[dict[str, str]],
) -> str:
    prompt = build_question_rewrite_prompt(question, history)
    rewritten_query = await generate_response(prompt)
    rewritten_query = rewritten_query.strip()

    if not rewritten_query:
        raise ValueError("Failed to rewrite the question into a standalone query.")

    return rewritten_query

async def get_question(payload: SearchRequest) -> str:
    if not payload.chat_history:
        return payload.query

    return await _rewrite_question(
        payload.query,
        [
            {"role": turn.role, "content": turn.content}
            for turn in payload.chat_history
        ],
    )

async def get_relevant_cvs_for_question(question: str) -> list[dict[str, Any]]:
    embedding = await generate_embedding_from_text(question)
    if not embedding:
        raise ValueError("Failed to generate an embedding for the question.")

    cvs = get_cvs_similar_to_embedding(
        embedding,
        top_k=CV_SEARCH_LIMIT,
    )
    return cvs

async def generate_response_from_cvs(
    question: str,
    cvs: list[dict[str, Any]],
) -> dict[str, Any]:
    prompt = build_prompt(question, cvs)
    response = await generate_response(prompt)
    if not response:
        raise ValueError("Failed to generate a response for question.")

    return {
        "response": response,
    }
