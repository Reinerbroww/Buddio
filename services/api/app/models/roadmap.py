from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=True)
    estimated_hours = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    topic = relationship("Topic", back_populates="roadmaps")
    steps = relationship("RoadmapStep", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapStep.order_number")


class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False, index=True)
    order_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)

    roadmap = relationship("Roadmap", back_populates="steps")
    lesson = relationship("Lesson", back_populates="step", cascade="all, delete-orphan", uselist=False)
