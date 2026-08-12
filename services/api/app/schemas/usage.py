from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime

class UsageResponse(BaseModel):
    chat_remaining: int
    roadmap_remaining: int
    quiz_remaining: int
    reset_date: Optional[date] = None
    limits: dict

class UsageHistoryItem(BaseModel):
    action: str
    detail: str
    created_at: datetime

class UsageHistoryResponse(BaseModel):
    items: List[UsageHistoryItem] = []
