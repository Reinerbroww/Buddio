from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.usage_service import UsageService

router = APIRouter(prefix="/usage", tags=["Usage"])

@router.get("/me")
def get_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UsageService(db).get_remaining(current_user)
