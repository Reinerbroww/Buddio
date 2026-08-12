from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicResponse, TopicDetail
from app.services.topic_service import TopicService

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.post("", response_model=TopicDetail, status_code=status.HTTP_201_CREATED)
def create_topic(
    data: TopicCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = TopicService(db).create(current_user, data)
    return topic

@router.get("", response_model=list[TopicDetail])
def list_topics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TopicService(db).list_for_user(current_user)

@router.get("/{topic_id}", response_model=TopicDetail)
def get_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TopicService(db).get(current_user, topic_id)

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    TopicService(db).delete(current_user, topic_id)
