from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter()

@router.get("/health", summary="Health check endpoint")
def health_check(db: Session = Depends(get_db)):
    db_ok = False
    try:
        # Perform a basic select 1 query to test db connectivity
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        # Logging or printing for debugging
        print(f"Database health check failed: {e}")
        db_ok = False

    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
        "services": {
            "api": "ok"
        }
    }
