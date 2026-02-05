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


# --- Redis Engine ---
_redis: Redis | None = None

def get_redis_engine() -> Redis:
    global _redis

    if _redis is None:
        _redis = Redis.from_url(settings.REDIS_URL,
                                decode_responses=True,
                                socket_connect_timeout=3,
                                socket_timeout=3,
                                retry_on_timeout=True,
                                health_check_interval=30
                                )

    return _redis


async def ping_redis() -> None:
    await get_redis_engine().ping()


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
        