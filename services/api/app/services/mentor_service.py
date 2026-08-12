from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.topic import Topic
from app.models.chat import ChatSession, ChatMessage
from app.ai import buddio_ai
from app.services.usage_service import UsageService


class MentorService:
    def __init__(self, db: Session):
        self.db = db

    def _get_owned_topic(self, user: User, topic_id: int) -> Topic:
        topic = self.db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == user.id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topik tidak ditemukan.")
        return topic

    def _session_for_topic(self, user: User, topic: Topic) -> ChatSession:
        session = (
            self.db.query(ChatSession)
            .filter(ChatSession.user_id == user.id, ChatSession.topic_id == topic.id)
            .order_by(ChatSession.created_at.desc())
            .first()
        )
        if session is None:
            session = ChatSession(user_id=user.id, topic_id=topic.id, title=topic.title)
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
        return session

    def chat(self, user: User, topic_id: int, message: str) -> dict:
        topic = self._get_owned_topic(user, topic_id)
        remaining = UsageService(self.db).check_and_decrement(user, "chat")

        session = self._session_for_topic(user, topic)
        history_rows = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == session.id)
            .order_by(ChatMessage.created_at.desc())
            .limit(10)
            .all()
        )
        history = [{"role": m.role, "content": m.message} for m in reversed(history_rows)]

        user_msg = ChatMessage(session_id=session.id, role="user", message=message)
        self.db.add(user_msg)

        answer, token_usage, mode = buddio_ai.chat(
            message=message,
            history=history,
            grade_level=user.grade_level or "sma",
            topic_title=topic.title,
        )

        assistant_msg = ChatMessage(
            session_id=session.id, role="assistant", message=answer, token_usage=token_usage
        )
        self.db.add(assistant_msg)
        self.db.commit()

        return {
            "answer": answer,
            "session_id": session.id,
            "mode": mode,
            "remaining": remaining,
        }

    def history(self, user: User, topic_id: int) -> list:
        self._get_owned_topic(user, topic_id)
        sessions = (
            self.db.query(ChatSession)
            .filter(ChatSession.user_id == user.id, ChatSession.topic_id == topic_id)
            .order_by(ChatSession.created_at.desc())
            .all()
        )
        return [
            {
                "id": s.id,
                "topic_id": s.topic_id,
                "title": s.title,
                "created_at": s.created_at,
                "messages": [
                    {"id": m.id, "role": m.role, "message": m.message, "created_at": m.created_at}
                    for m in s.messages
                ],
            }
            for s in sessions
        ]

    def delete_history(self, user: User, topic_id: int) -> None:
        self._get_owned_topic(user, topic_id)
        sessions = self.db.query(ChatSession).filter(
            ChatSession.user_id == user.id, ChatSession.topic_id == topic_id
        ).all()
        for s in sessions:
            self.db.delete(s)
        self.db.commit()
