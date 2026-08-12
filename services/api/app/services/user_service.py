from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, ChangePassword
from app.models.user import User
from app.core import security
from fastapi import HTTPException, status
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> User:
        existing_user = self.repository.get_by_email(user_in.email)
        if existing_user:
            raise ValueError("Email sudah terdaftar.")

        hashed_password = security.get_password_hash(user_in.password)
        return self.repository.create(user_in, hashed_password)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.repository.get_by_email(email)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def update_user_profile(self, user: User, user_update: UserUpdate) -> User:
        return self.repository.update(user, user_update)

    def set_grade_level(self, user: User, grade_level: str) -> User:
        user.grade_level = grade_level
        self.db.commit()
        self.db.refresh(user)
        return user

    def set_learning_goal(self, user: User, goal: str) -> User:
        user.learning_goal = goal
        self.db.commit()
        self.db.refresh(user)
        return user

    def change_password(self, user: User, old_password: str, new_password: str) -> None:
        if not security.verify_password(old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password lama salah.",
            )
        user.hashed_password = security.get_password_hash(new_password)
        self.db.commit()
