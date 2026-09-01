from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.topic import Topic
from app.models.roadmap import Roadmap, RoadmapStep
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.ai import buddio_ai
from app.services.usage_service import UsageService


class RoadmapService:
    def __init__(self, db: Session):
        self.db = db

    def _get_owned_topic(self, user: User, topic_id: int) -> Topic:
        topic = self.db.query(Topic).filter(Topic.id == topic_id, Topic.user_id == user.id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topik tidak ditemukan.")
        return topic

    def _get_owned_roadmap(self, user: User, roadmap_id: int) -> Roadmap:
        roadmap = (
            self.db.query(Roadmap)
            .join(Topic, Roadmap.topic_id == Topic.id)
            .filter(Roadmap.id == roadmap_id, Topic.user_id == user.id)
            .first()
        )
        if not roadmap:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap tidak ditemukan.")
        return roadmap

    def generate(self, user: User, topic_id: int, goal: str = "", regenerate: bool = False) -> dict:
        topic = self._get_owned_topic(user, topic_id)

        # Reuse existing roadmap unless explicitly regenerating.
        if not regenerate:
            existing = (
                self.db.query(Roadmap)
                .filter(Roadmap.topic_id == topic_id)
                .order_by(Roadmap.created_at.desc())
                .first()
            )
            if existing:
                return self.serialize(self._get_owned_roadmap(user, existing.id), mode="cached")

        UsageService(self.db).check_and_decrement(user, "roadmap")

        data, mode = buddio_ai.generate_roadmap(topic.title, user.grade_level or "sma", goal)

        # Replace the previous roadmap for this topic to keep a single active plan.
        old_roadmaps = self.db.query(Roadmap).filter(Roadmap.topic_id == topic_id).all()
        for old in old_roadmaps:
            self.db.delete(old)
        self.db.commit()

        roadmap = Roadmap(
            topic_id=topic.id,
            title=data.get("title", f"Roadmap {topic.title}"),
            difficulty=data.get("difficulty"),
            estimated_hours=data.get("estimated_hours"),
        )
        self.db.add(roadmap)
        self.db.flush()

        for step in data.get("steps", []):
            rs = RoadmapStep(
                roadmap_id=roadmap.id,
                order_number=step.get("order_number", 1),
                title=step.get("title", "Langkah"),
                description=step.get("description"),
            )
            self.db.add(rs)
            self.db.flush()
            # Create the lesson shell WITHOUT seeding content: the step's short
            # description is only a roadmap summary. The real, full materi is generated
            # later (on the intro/"Mulai Belajar" screen) so the first-time flow shows.
            lesson = Lesson(
                roadmap_step_id=rs.id,
                content=None,
                source="AI Buddio",
            )
            self.db.add(lesson)

        self.db.commit()
        self.db.refresh(roadmap)
        return self.serialize(self._get_owned_roadmap(user, roadmap.id), mode=mode)

    def get(self, user: User, roadmap_id: int) -> dict:
        roadmap = self._get_owned_roadmap(user, roadmap_id)
        return self.serialize(roadmap, mode="cached")

    def get_latest_for_topic(self, user: User, topic_id: int) -> dict:
        topic = self._get_owned_topic(user, topic_id)
        roadmap = (
            self.db.query(Roadmap)
            .filter(Roadmap.topic_id == topic.id)
            .order_by(Roadmap.created_at.desc())
            .first()
        )
        if not roadmap:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap belum dibuat untuk topik ini.")
        return self.serialize(roadmap, mode="cached")

    def update_step(self, user: User, step_id: int, completed: bool) -> dict:
        step = (
            self.db.query(RoadmapStep)
            .join(Roadmap, RoadmapStep.roadmap_id == Roadmap.id)
            .join(Topic, Roadmap.topic_id == Topic.id)
            .filter(RoadmapStep.id == step_id, Topic.user_id == user.id)
            .first()
        )
        if not step:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Langkah roadmap tidak ditemukan.")

        step.completed = completed
        roadmap = step.roadmap
        total = len(roadmap.steps)
        done = sum(1 for s in roadmap.steps if s.completed)
        pct = round((done / total) * 100) if total else 0

        progress = self.db.query(Progress).filter(Progress.topic_id == roadmap.topic_id).first()
        if progress:
            progress.completion_percentage = pct
            progress.current_step = None if pct == 100 else step.title

        self.db.commit()
        return {"step_id": step.id, "completed": step.completed, "completion_percentage": pct}

    def serialize(self, roadmap: Roadmap, mode: str = "cached") -> dict:
        steps = roadmap.steps
        total = len(steps)
        done = sum(1 for s in steps if s.completed)
        return {
            "id": roadmap.id,
            "topic_id": roadmap.topic_id,
            "title": roadmap.title,
            "difficulty": roadmap.difficulty,
            "estimated_hours": roadmap.estimated_hours,
            "created_at": roadmap.created_at,
            "mode": mode,
            "completion_percentage": round((done / total) * 100) if total else 0,
            "steps": [
                {
                    "id": s.id,
                    "order_number": s.order_number,
                    "title": s.title,
                    "description": s.description,
                    "completed": s.completed,
                    "lesson_id": s.lesson.id if s.lesson else None,
                }
                for s in steps
            ],
        }
