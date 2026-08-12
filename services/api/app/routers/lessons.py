from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.lesson import Lesson
from app.models.roadmap import RoadmapStep, Roadmap
from app.models.topic import Topic
from app.schemas.lesson import LessonResponse
from app.services.progress_service import ProgressService
from app.services.roadmap_service import RoadmapService

router = APIRouter(prefix="/lessons", tags=["Lessons"])

def _owned_lesson(db: Session, user: User, lesson_id: int) -> Lesson:
    lesson = (
        db.query(Lesson)
        .join(RoadmapStep, Lesson.roadmap_step_id == RoadmapStep.id)
        .join(Roadmap, RoadmapStep.roadmap_id == Roadmap.id)
        .join(Topic, Roadmap.topic_id == Topic.id)
        .filter(Lesson.id == lesson_id, Topic.user_id == user.id)
        .first()
    )
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materi tidak ditemukan.")
    return lesson

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _owned_lesson(db, current_user, lesson_id)

@router.patch("/{lesson_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
def complete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    lesson = _owned_lesson(db, current_user, lesson_id)
    step = lesson.step
    if not step.completed:
        RoadmapService(db).update_step(current_user, step.id, True)
    ProgressService(db).add_study_minutes(current_user, step.roadmap.topic_id, minutes=15)
