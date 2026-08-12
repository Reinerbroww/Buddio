from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.topic import Topic
from app.models.progress import Progress
from app.models.roadmap import Roadmap
from app.models.quiz import QuizAttempt
from app.models.chat import ChatMessage, ChatSession
from app.services.usage_service import UsageService


class ProgressService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self, user: User) -> list:
        rows = (
            self.db.query(Progress)
            .join(Topic, Progress.topic_id == Topic.id)
            .filter(Progress.user_id == user.id)
            .order_by(Topic.created_at.desc())
            .all()
        )
        return [
            {
                "topic_id": p.topic_id,
                "topic_title": p.topic.title,
                "completion_percentage": p.completion_percentage,
                "study_minutes": p.study_minutes,
                "last_access": p.last_access,
                "current_step": p.current_step,
            }
            for p in rows
        ]

    def statistics(self, user: User) -> dict:
        usage = UsageService(self.db).get_remaining(user)
        progresses = self.db.query(Progress).filter(Progress.user_id == user.id).all()
        topics = self.db.query(Topic).filter(Topic.user_id == user.id).count()

        total_minutes = sum(p.study_minutes for p in progresses)
        avg = round(sum(p.completion_percentage for p in progresses) / len(progresses)) if progresses else 0

        # Compute streak from daily activity (chat messages + quiz attempts).
        streak = self._compute_streak(user)

        return {
            "study_hours": total_minutes // 60,
            "topics": topics,
            "streak": streak,
            "completion": avg,
            "chat_remaining": usage["chat_remaining"],
            "roadmap_remaining": usage["roadmap_remaining"],
            "quiz_remaining": usage["quiz_remaining"],
        }

    def _compute_streak(self, user: User) -> int:
        session_ids = [s.id for s in self.db.query(ChatSession).filter(ChatSession.user_id == user.id).all()]
        active_days = set()
        if session_ids:
            for m in self.db.query(ChatMessage).filter(ChatMessage.session_id.in_(session_ids)).all():
                active_days.add(m.created_at.date())
        for a in self.db.query(QuizAttempt).filter(QuizAttempt.user_id == user.id).all():
            active_days.add(a.created_at.date())

        streak = 0
        day = date.today()
        while day in active_days:
            streak += 1
            day -= timedelta(days=1)
        return streak

    def add_study_minutes(self, user: User, topic_id: int, minutes: int = 15) -> None:
        progress = (
            self.db.query(Progress)
            .filter(Progress.user_id == user.id, Progress.topic_id == topic_id)
            .first()
        )
        if progress:
            progress.study_minutes = (progress.study_minutes or 0) + minutes
            progress.last_access = date.today()
            self.db.commit()
