from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProgressResponse(BaseModel):
    topic_id: int
    topic_title: str
    completion_percentage: int
    study_minutes: int
    last_access: Optional[datetime] = None
    current_step: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class StatisticsResponse(BaseModel):
    study_hours: int
    topics: int
    streak: int
    completion: int
    chat_remaining: int
    roadmap_remaining: int
    quiz_remaining: int
