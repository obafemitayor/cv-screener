from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    chat_history: list[ChatMessage] = Field(default_factory=list)


class SearchResponse(BaseModel):
    response: str
