from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TopicCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TopicResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
    progress_percentage: int = 0
    has_roadmap: bool = False

    model_config = ConfigDict(from_attributes=True)

class TopicDetail(TopicResponse):
    pass
