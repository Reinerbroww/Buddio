from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("/all")
def list_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProgressService(db).list_all(current_user)

@router.get("/statistics")
def statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProgressService(db).statistics(current_user)
