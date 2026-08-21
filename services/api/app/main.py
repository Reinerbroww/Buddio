from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import health, auth, users, onboarding, topics, roadmaps, lessons, mentor, quiz, progress, usage, settings as settings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    import app.models  # noqa: F401 - register all models
    Base.metadata.create_all(bind=engine)
    _safe_migrate()
    yield


def _safe_migrate():
    """Run safe, idempotent schema migrations that create_all won't handle."""
    from sqlalchemy import text
    migrations = [
        "ALTER TABLE lessons ADD COLUMN IF NOT EXISTS video_urls JSON",
    ]
    with engine.connect() as conn:
        for sql in migrations:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                pass

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Buddio AI Learning Companion Backend API",
    lifespan=lifespan
)

# CORS middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(onboarding.router, prefix="/api")
app.include_router(topics.router, prefix="/api")
app.include_router(roadmaps.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(mentor.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(usage.router, prefix="/api")
app.include_router(settings_router.router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Buddio API!",
        "documentation": "/docs"
    }
