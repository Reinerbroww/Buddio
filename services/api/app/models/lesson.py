from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_step_id = Column(Integer, ForeignKey("roadmap_steps.id"), nullable=False, index=True)
    content = Column(Text, nullable=True)
    source = Column(String, nullable=True)  # e.g. "AI Buddio"

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    step = relationship("RoadmapStep", back_populates="lesson")
