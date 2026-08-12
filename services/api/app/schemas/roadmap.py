from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class RoadmapGenerate(BaseModel):
    topic_id: int
    goal: Optional[str] = None
    regenerate: bool = False

class RoadmapStepCreate(BaseModel):
    order_number: int
    title: str
    description: Optional[str] = None

class RoadmapStepResponse(BaseModel):
    id: int
    order_number: int
    title: str
    description: Optional[str] = None
    completed: bool
    lesson_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class RoadmapResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    difficulty: Optional[str] = None
    estimated_hours: Optional[float] = None
    created_at: datetime
    steps: List[RoadmapStepResponse] = []
    completion_percentage: int = 0
    mode: Optional[str] = None  # "gemini" | "mock" | "cached"

    model_config = ConfigDict(from_attributes=True)

class StepUpdate(BaseModel):
    completed: bool
