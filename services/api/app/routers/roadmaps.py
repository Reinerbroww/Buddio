from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.roadmap import RoadmapGenerate, RoadmapResponse, StepUpdate
from app.services.roadmap_service import RoadmapService

router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])

@router.post("/generate", response_model=RoadmapResponse)
def generate_roadmap(
    data: RoadmapGenerate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).generate(
        current_user, data.topic_id, goal=data.goal or "", regenerate=data.regenerate
    )

@router.get("/topic/{topic_id}", response_model=RoadmapResponse)
def get_latest_roadmap(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).get_latest_for_topic(current_user, topic_id)

@router.get("/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap(
    roadmap_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).get(current_user, roadmap_id)

@router.patch("/steps/{step_id}", response_model=dict)
def update_step(
    step_id: int,
    data: StepUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RoadmapService(db).update_step(current_user, step_id, data.completed)
