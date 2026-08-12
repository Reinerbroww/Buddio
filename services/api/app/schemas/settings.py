from pydantic import BaseModel, ConfigDict
from typing import Optional

class SettingsUpdate(BaseModel):
    theme: Optional[str] = None
    notification: Optional[bool] = None
    language: Optional[str] = None
    daily_goal: Optional[int] = None

class SettingsResponse(BaseModel):
    theme: str
    notification: bool
    language: str
    daily_goal: int

    model_config = ConfigDict(from_attributes=True)
