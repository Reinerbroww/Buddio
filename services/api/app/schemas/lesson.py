from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class LessonResponse(BaseModel):
    id: int
    roadmap_step_id: int
    content: Optional[str] = None
    source: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
