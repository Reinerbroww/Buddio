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
from app.ai import buddio_ai

router = APIRouter(prefix="/lessons", tags=["Lessons"])


def _owned_lesson_with_context(db: Session, user: User, lesson_id: int) -> dict:
    """Fetch lesson and return it with step/topic context."""
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
    step = lesson.step
    topic = step.roadmap.topic
    return {
        "id": lesson.id,
        "roadmap_step_id": lesson.roadmap_step_id,
        "content": lesson.content,
        "source": lesson.source,
        "video_urls": lesson.video_urls or [],
        "step_title": step.title,
        "step_description": step.description,
        "topic_title": topic.title,
        "topic_id": topic.id,
        "created_at": lesson.created_at,
    }


def _owned_step(db: Session, user: User, step_id: int) -> RoadmapStep:
    step = (
        db.query(RoadmapStep)
        .join(Roadmap, RoadmapStep.roadmap_id == Roadmap.id)
        .join(Topic, Roadmap.topic_id == Topic.id)
        .filter(RoadmapStep.id == step_id, Topic.user_id == user.id)
        .first()
    )
    if not step:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Langkah roadmap tidak ditemukan.")
    return step


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _owned_lesson_with_context(db, current_user, lesson_id)


@router.post("/generate/{step_id}", response_model=LessonResponse)
def generate_lesson_content(
    step_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate rich lesson content for a roadmap step using AI."""
    step = _owned_step(db, current_user, step_id)
    topic = step.roadmap.topic
    lesson = step.lesson

    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Materi tidak ditemukan.")

    lesson_data, mode = buddio_ai.generate_lesson(
        step_title=step.title,
        topic_title=topic.title,
        grade_level=current_user.grade_level or "sma",
        step_description=step.description or "",
    )

    lesson.content = lesson_data.get("content", lesson.content)
    lesson.video_urls = lesson_data.get("videos", [])
    lesson.source = f"AI Buddio ({mode})"
    db.commit()
    db.refresh(lesson)

    return {
        "id": lesson.id,
        "roadmap_step_id": lesson.roadmap_step_id,
        "content": lesson.content,
        "source": lesson.source,
        "video_urls": lesson.video_urls or [],
        "step_title": step.title,
        "step_description": step.description,
        "topic_title": topic.title,
        "topic_id": topic.id,
        "created_at": lesson.created_at,
    }


@router.patch("/{lesson_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
def complete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    lesson_data = _owned_lesson_with_context(db, current_user, lesson_id)
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    step = lesson.step
    if not step.completed:
        RoadmapService(db).update_step(current_user, step.id, True)
    ProgressService(db).add_study_minutes(current_user, step.roadmap.topic_id, minutes=15)
