from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.quiz import QuizGenerate, QuizResponse, QuizSubmit, QuizAttemptResponse
from app.services.assessment_service import AssessmentService

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/generate", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def generate_quiz(
    data: QuizGenerate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AssessmentService(db).generate(current_user, data.topic_id, data.count)

@router.get("/topic/{topic_id}", response_model=list[QuizResponse])
def list_quizzes(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AssessmentService(db).list_for_topic(current_user, topic_id)

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AssessmentService(db).get(current_user, quiz_id)

@router.post("/{quiz_id}/submit", response_model=QuizAttemptResponse)
def submit_quiz(
    quiz_id: int,
    data: QuizSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AssessmentService(db).submit(current_user, quiz_id, data.answers)

@router.get("/attempts/{attempt_id}", response_model=dict)
def get_attempt(
    attempt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AssessmentService(db).get_attempt(current_user, attempt_id)
