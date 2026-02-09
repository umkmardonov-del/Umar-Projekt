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
    HOST_OPEN: str = "0.0.0.0"
    HOST_LOCAL: str = "127.0.0.1"
    PORT: int = 5000
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

    # --- Datenbank: Redis ---
    REDIS_URL: str = Field(default="redis://user:password@host:port/database",
                           description="Redis URL.")


    # --- Sessions ---
    SESSION_MAX_AGE_SEC: int = 3600
    SESSION_ROLLING: bool = True
    SESSION_COOKIE_NAME: str = "session-cookie"

    # --- Cookies ---
    COOKIE_DOMAIN: str = ""
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"
    COOKIE_PATH: str = ""


settings = Settings()
