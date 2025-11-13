# --- Lifespan für Datenbank ---
# --- path: /app/core/lifespan.py ---

from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool
    )
    async with engine.connect() as conn:
        await conn.scalar(text("SELECT 1"))
        print("PostgreSQL DB verbunden.")
    yield
    await engine.dispose()
    print("Verbindung zu PostgreSQL DB geschlossen.")
