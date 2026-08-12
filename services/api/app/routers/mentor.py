from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatIn, ChatResponse, ChatHistoryResponse
from app.services.mentor_service import MentorService

router = APIRouter(prefix="/mentor", tags=["Mentor"])

@router.post("/chat", response_model=ChatResponse)
def chat(
    data: ChatIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MentorService(db).chat(current_user, data.topic_id, data.message)

@router.get("/history/{topic_id}", response_model=list[ChatHistoryResponse])
def chat_history(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MentorService(db).history(current_user, topic_id)

@router.delete("/history/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_history(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    MentorService(db).delete_history(current_user, topic_id)
