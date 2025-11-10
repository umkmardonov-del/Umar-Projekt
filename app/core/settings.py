# --- Pydantic-Settings ---
# --- path: /app/core/settings.py ---

from __future__ import annotations

from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        case_sensitive=False,
    )

    # --- App-Basics ---
    ENV: Literal["development", "staging", "production"] = "development"
    APP_NAME: str = "fastapi-app"
    API_PREFIX: str = ""
    HOST: str = "0.0.0.0"
    PORT: int = 8000    
    RELOAD: bool = True

    # --- Logging ---
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_JSON: bool = False
    LOG_ACCESS: bool = True
    LOG_SQL: bool = False

    # --- Datenbank: PostgreSQL ---
    DATABASE_URL: str = Field(default="Database+Driver://user:password@host:port/database",
                              description="PostgreSQL URL.")
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False
    DB_POOL_PRE_PING: bool = True

settings = Settings()
