# --- Dependencies für Dependency Injection ---
# --- path: /app/core/deps.py ---

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.db.session import AsyncSessionLocal


async def postgres_dep() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise