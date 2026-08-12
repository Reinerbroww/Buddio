from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="topics")
    roadmaps = relationship("Roadmap", back_populates="topic", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="topic", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="topic", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="topic", cascade="all, delete-orphan", uselist=False)
