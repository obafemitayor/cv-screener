import logging

from fastapi import APIRouter, HTTPException, Request

from app.schemas.search import SearchRequest, SearchResponse
from app.services.search_service import (
    get_question,
    get_relevant_cvs_for_question,
    generate_response_from_cvs,
)
from app.utils.rate_limit import limiter


router = APIRouter(tags=["search"])
logger = logging.getLogger(__name__)


@router.post("/search", response_model=SearchResponse)
@limiter.limit("10/minute")
async def search_cvs(request: Request, payload: SearchRequest) -> SearchResponse:
    try:
        query = await get_question(payload)
        cvs = await get_relevant_cvs_for_question(query)
        if not cvs:
            return SearchResponse(
                response="I could not find any indexed CV content to answer the question.",
            )

        result = await generate_response_from_cvs(
            query,
            cvs,
        )
    except Exception as exc:
        logger.exception("CV search failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the question.",
        ) from exc

    return SearchResponse(**result)
