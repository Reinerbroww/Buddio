from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.user import GRADE_LEVELS
from app.services.user_service import UserService

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

class GradeLevelIn(BaseModel):
    grade_level: str

class LearningGoalIn(BaseModel):
    goal: str

@router.post("/grade-level", response_model=UserResponse)
def set_grade_level(
    data: GradeLevelIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    grade = data.grade_level.strip().lower()
    if grade not in GRADE_LEVELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Jenjang tidak valid. Pilih salah satu: {', '.join(sorted(GRADE_LEVELS))}",
        )
    return UserService(db).set_grade_level(current_user, grade)

@router.post("/learning-goal", response_model=UserResponse)
def set_learning_goal(
    data: LearningGoalIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    goal = data.goal.strip()
    if not goal:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tujuan belajar tidak boleh kosong.")
    return UserService(db).set_learning_goal(current_user, goal)
