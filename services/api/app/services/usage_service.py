from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.usage import AIUsage

LIMITS = {
    "chat": settings.QUOTA_CHAT_DAILY,
    "roadmap": settings.QUOTA_ROADMAP_DAILY,
    "quiz": settings.QUOTA_QUIZ_DAILY,
}


class UsageService:
    def __init__(self, db: Session):
        self.db = db

    def _ensure_today(self, user: User) -> AIUsage:
        usage = self.db.query(AIUsage).filter(AIUsage.user_id == user.id).first()
        today = date.today()
        if usage is None:
            usage = AIUsage(user_id=user.id, chat_used=0, quiz_used=0, roadmap_used=0, reset_date=today)
            self.db.add(usage)
            self.db.commit()
            self.db.refresh(usage)
        elif usage.reset_date != today:
            usage.chat_used = 0
            usage.quiz_used = 0
            usage.roadmap_used = 0
            usage.reset_date = today
            self.db.commit()
            self.db.refresh(usage)
        return usage

    def get_remaining(self, user: User) -> dict:
        usage = self._ensure_today(user)
        return {
            "chat_remaining": max(0, LIMITS["chat"] - usage.chat_used),
            "roadmap_remaining": max(0, LIMITS["roadmap"] - usage.roadmap_used),
            "quiz_remaining": max(0, LIMITS["quiz"] - usage.quiz_used),
            "reset_date": usage.reset_date,
            "limits": LIMITS,
        }

    def check_and_decrement(self, user: User, action: str) -> int:
        """Check quota for `action` (chat|roadmap|quiz) and consume one unit.

        Raises 429 when the daily quota is exhausted. Returns remaining count.
        """
        usage = self._ensure_today(user)
        if action == "chat":
            used, limit = usage.chat_used, LIMITS["chat"]
        elif action == "roadmap":
            used, limit = usage.roadmap_used, LIMITS["roadmap"]
        elif action == "quiz":
            used, limit = usage.quiz_used, LIMITS["quiz"]
        else:
            raise ValueError(f"Unknown AI action: {action}")

        if used >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "message": "Kuota AI harianmu sudah habis. Silakan coba lagi besok.",
                    "action": action,
                    "remaining": 0,
                    "reset_date": str(usage.reset_date),
                },
            )

        if action == "chat":
            usage.chat_used = used + 1
        elif action == "roadmap":
            usage.roadmap_used = used + 1
        else:
            usage.quiz_used = used + 1
        self.db.commit()
        return limit - (used + 1)
