from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class AIUsage(Base):
    __tablename__ = "ai_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, unique=True)
    chat_used = Column(Integer, default=0)
    quiz_used = Column(Integer, default=0)
    roadmap_used = Column(Integer, default=0)
    reset_date = Column(Date, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
