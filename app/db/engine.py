# --- Engine-Connection für DB-Sessions ---
# --- path: /app/db/engine.py ---

from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.core.settings import settings


def get_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=settings.DB_POOL_PRE_PING
    )