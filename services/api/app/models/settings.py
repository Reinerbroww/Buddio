from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, unique=True)
    theme = Column(String, default="light")
    notification = Column(Boolean, default=True)
    language = Column(String, default="id")
    daily_goal = Column(Integer, default=30)  # minutes
