from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    completion_percentage = Column(Integer, default=0)
    study_minutes = Column(Integer, default=0)
    last_access = Column(DateTime(timezone=True), nullable=True)
    current_step = Column(String, nullable=True)

    topic = relationship("Topic", back_populates="progress")
