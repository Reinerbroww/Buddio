from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ChatIn(BaseModel):
    topic_id: int
    message: str

class ChatRequest(BaseModel):
    topic_id: int
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatSessionResponse(BaseModel):
    id: int
    topic_id: int
    title: Optional[str] = None
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ChatResponse(BaseModel):
    answer: str
    session_id: int
    mode: str  # "gemini" | "mock"
    remaining: int

class ChatHistoryResponse(BaseModel):
    id: int
    topic_id: int
    title: Optional[str] = None
    created_at: datetime
    messages: List[ChatMessageResponse] = []
