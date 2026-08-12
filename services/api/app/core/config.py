import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Determine the workspace root relative to this file
# This config is located at services/api/app/core/config.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))  # services/api
WORKSPACE_ROOT = os.path.dirname(API_DIR)               # d:\SF Group\Buddio

class Settings(BaseSettings):
    APP_NAME: str = "Buddio API"
    APP_ENV: str = "development"
    # Always override SECRET_KEY via .env in any non-local environment.
    SECRET_KEY: str = "buddio_super_secret_key_development_only_12345"
    DATABASE_URL: str = Field(default="postgresql+psycopg://buddio_user:buddio_password@localhost:5432/buddio_db?connect_timeout=3")

    GEMINI_API_KEY: Optional[str] = Field(default=None)
    GEMINI_MODEL: str = "gemini-flash-latest"

    # CORS - keep explicit in production.
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Daily AI quota defaults.
    QUOTA_CHAT_DAILY: int = 20
    QUOTA_ROADMAP_DAILY: int = 2
    QUOTA_QUIZ_DAILY: int = 3

    # When True, the AI layer uses rule-based generators even if a key is set.
    FORCE_MOCK_AI: bool = False

    model_config = SettingsConfigDict(
        env_file=(
            os.path.join(WORKSPACE_ROOT, ".env"),
            os.path.join(API_DIR, ".env"),
            ".env"
        ),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
