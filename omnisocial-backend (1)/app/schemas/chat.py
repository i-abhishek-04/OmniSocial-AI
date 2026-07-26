"""
Pydantic request/response models for chat endpoints.
"""
from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatMessageItem(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageResponse(BaseModel):
    reply: ChatMessageItem


class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessageItem]
