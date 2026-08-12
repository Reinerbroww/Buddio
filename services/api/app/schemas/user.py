from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime

GRADE_LEVELS = {"sd", "smp", "sma", "mahasiswa", "self_learner"}

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    grade_level: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: Optional[str] = None
    grade_level: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    grade_level: Optional[str] = None
    learning_goal: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None

class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    grade_level: Optional[str] = None
    learning_goal: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
