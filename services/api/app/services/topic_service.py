from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.topic import Topic
from app.models.progress import Progress
from app.models.roadmap import Roadmap
from app.schemas.topic import TopicCreate


class TopicService:
    def __init__(self, db: Session):
        self.db = db

    def _get_owned(self, user: User, topic_id: int) -> Topic:
        topic = self.db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == user.id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topik tidak ditemukan.")
        return topic

    def create(self, user: User, data: TopicCreate) -> Topic:
        topic = Topic(user_id=user.id, title=data.title.strip(), description=data.description)
        self.db.add(topic)
        self.db.flush()
        progress = Progress(user_id=user.id, topic_id=topic.id, completion_percentage=0, study_minutes=0)
        self.db.add(progress)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def list_for_user(self, user: User):
        topics = self.db.query(Topic).filter(Topic.user_id == user.id).order_by(Topic.created_at.desc()).all()
        result = []
        for topic in topics:
            result.append(self._with_progress(topic))
        return result

    def get(self, user: User, topic_id: int):
        topic = self._get_owned(user, topic_id)
        return self._with_progress(topic)

    def delete(self, user: User, topic_id: int) -> None:
        topic = self._get_owned(user, topic_id)
        self.db.delete(topic)
        self.db.commit()

    def _with_progress(self, topic: Topic) -> dict:
        progress = self.db.query(Progress).filter(Progress.topic_id == topic.id).first()
        has_roadmap = self.db.query(Roadmap).filter(Roadmap.topic_id == topic.id).first() is not None
        return {
            "id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "status": topic.status,
            "created_at": topic.created_at,
            "progress_percentage": progress.completion_percentage if progress else 0,
            "has_roadmap": has_roadmap,
        }
