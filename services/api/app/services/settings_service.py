from sqlalchemy.orm import Session

from app.models.user import User
from app.models.settings import UserSettings
from app.schemas.settings import SettingsUpdate


class SettingsService:
    def __init__(self, db: Session):
        self.db = db

    def _get(self, user: User) -> UserSettings:
        settings = self.db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
        if settings is None:
            settings = UserSettings(user_id=user.id)
            self.db.add(settings)
            self.db.commit()
            self.db.refresh(settings)
        return settings

    def get(self, user: User) -> UserSettings:
        return self._get(user)

    def update(self, user: User, data: SettingsUpdate) -> UserSettings:
        settings = self._get(user)
        payload = data.model_dump(exclude_unset=True)
        for field, value in payload.items():
            setattr(settings, field, value)
        self.db.commit()
        self.db.refresh(settings)
        return settings
