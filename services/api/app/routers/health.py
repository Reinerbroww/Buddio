from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health", summary="Health check endpoint")
def health_check(db: Session = Depends(get_db)):
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        print(f"Database health check failed: {e}")
        db_ok = False

    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
        "gemini_key_set": bool(settings.GEMINI_API_KEY),
        "gemini_model": settings.GEMINI_MODEL,
        "force_mock": settings.FORCE_MOCK_AI,
        "app_env": settings.APP_ENV,
    }

@router.get("/debug-ai")
def debug_ai():
    result = {"key_set": bool(settings.GEMINI_API_KEY), "model": settings.GEMINI_MODEL}
    try:
        from google import genai
        result["import_ok"] = True
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        result["client_ok"] = True
        from google.genai import types
        resp = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents="Say exactly: OK",
            config=types.GenerateContentConfig(
                system_instruction="You are Buddio. Reply in Bahasa Indonesia.",
                max_output_tokens=2048,
                temperature=0.6,
            ),
        )
        result["api_ok"] = True
        result["response"] = (resp.text or "")[:200]
    except Exception as e:
        result["error"] = str(e)
    return result
