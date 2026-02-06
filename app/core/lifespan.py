# --- Lifespan für Datenbank ---
# --- path: /app/core/lifespan.py ---

from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from logging import getLogger
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.engines import ping_redis, close_redis
from app.core.settings import settings


logger = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool
    )
    async with engine.connect() as conn:
        await conn.scalar(text("SELECT 1"))
        logger.info("PostgreSQL DB verbunden.")
    await ping_redis()
    logger.info("Redis DB verbunden.")
    yield
    await engine.dispose()
    logger.info("Verbindung zu PostgreSQL DB geschlossen.")
    await close_redis()
    logger.info("Verbindung zu Redis DB geschlossen.")
