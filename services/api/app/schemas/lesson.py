from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class VideoItem(BaseModel):
    title: str
    url: str
    description: Optional[str] = None

class LessonResponse(BaseModel):
    id: int
    roadmap_step_id: int
    content: Optional[str] = None
    source: Optional[str] = None
    video_urls: Optional[List[VideoItem]] = None
    step_title: Optional[str] = None
    step_description: Optional[str] = None
    topic_title: Optional[str] = None
    topic_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
