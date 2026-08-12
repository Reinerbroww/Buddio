from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime

class QuizGenerate(BaseModel):
    topic_id: int
    count: int = 5

class QuizQuestionResponse(BaseModel):
    id: int
    question: str
    options: Optional[List[str]] = None
    explanation: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class QuizResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    generated_by_ai: bool
    created_at: datetime
    mode: Optional[str] = None  # "gemini" | "mock" | "cached"
    questions: List[QuizQuestionResponse] = []

    model_config = ConfigDict(from_attributes=True)

class QuizSubmit(BaseModel):
    quiz_id: int
    answers: Dict[int, int]  # {question_id: option_index}

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    score: int
    total: int
    feedback: Optional[str] = None
    answers: Optional[Dict] = None
    created_at: datetime
    details: Optional[List[Dict]] = None

    model_config = ConfigDict(from_attributes=True)
