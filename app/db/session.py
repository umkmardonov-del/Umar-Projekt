# --- Sessionfabrik für AsyncSessions ---
# --- path: /app/core/session.py ---
from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Final

from .engine import get_engine


engine = get_engine()


# --- Fabrikfunktion: Liefert AsyncSessions ---
AsyncSessionLocal: Final[async_sessionmaker] = async_sessionmaker[AsyncSession](
    bind=engine,
    expire_on_commit=False,
)