# --- Dependencies für Dependency Injection ---
# --- path: /app/core/deps.py ---

from __future__ import annotations

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.db.engines import get_redis_engine
from app.db.session import AsyncSessionLocal
from app.security.session_store import SessionStore


async def postgres_dep() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def redis_dep() -> Redis:
    return get_redis_engine()


async def session_store_dep(client: Redis = Depends(redis_dep)) -> SessionStore:
    return SessionStore(client=client)
