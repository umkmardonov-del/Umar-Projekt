# --- Wrapper um Redis-Methoden und Pipelines ---
# --- path: /app/db/session_data.py ---

from logging import getLogger
from json import loads, dumps, JSONDecodeError
from redis.asyncio import Redis
from typing import Any, Final, Optional

from app.core.exceptions import (JSONSerializationError, CorruptSessionError, JSONDeserializationError,
                                 SessionTimeoutError)
from app.core.settings import settings
from app.security.session_data import SessionData

logger = getLogger(__name__)

class SessionStore:

    _KEY_PREFIX: Final[str] = "sess:"

    def __init__(self, client: Redis):
        self.client: Redis = client

    async def login_user(self,
                         session_id: str,
                         session_data: SessionData,
                         ttl_sec: int = settings.SESSION_MAX_AGE_SEC) -> None:

        user_id: str = session_data["user_id"]
        if not session_id or not user_id:
            logger.error("Variablen 'user_id' und/oder 'session_id' haben ungültige Werte!")
            raise CorruptSessionError()

        try:
            payload = dumps(session_data, separators=(",", ":"))

        except (ValueError, TypeError, RecursionError) as e:
            raise JSONSerializationError() from e

        session_key = f"{self._KEY_PREFIX}{session_id}"
        set_key = f"user:{user_id}:sessions"

        async with self.client.pipeline() as pipeline:
            pipeline.setex(session_key, ttl_sec, payload)
            pipeline.sadd(set_key, session_id)
            await pipeline.execute()

    async def logout_user(self,
                          session_id: str,
                          user_id: str) -> None:

        if not session_id or not user_id:
            logger.error("Variablen 'user_id' und/oder 'session_id' haben ungültige Werte!")
            raise CorruptSessionError()

        session_key = f"{self._KEY_PREFIX}{session_id}"
        set_key = f"user:{user_id}:sessions"

        async with self.client.pipeline() as pipeline:
            pipeline.delete(session_key)
            pipeline.srem(set_key, session_id)
            await pipeline.execute()

    async def get(self,
                  session_id: str) -> Optional[SessionData]:

        if not session_id:
            logger.error("Variable 'session_id' hat einen ungültigen Wert!")
            raise CorruptSessionError()

        session_key = f"{self._KEY_PREFIX}{session_id}"

        raw_data: str = await self.client.get(session_key)
        if raw_data is None:
            raise SessionTimeoutError()

        try:
            session_data = loads(raw_data)

        except Exception as e:
            raise JSONDeserializationError() from e

        if isinstance(session_data, dict):
            return session_data
        else:
            raise ValueError("Falscher type(session_data)")

    async def expire(self,
                     session_id: str,
                     ttl_sec: int = settings.SESSION_MAX_AGE_SEC) -> int:

        if not session_id:
            logger.error("Variable 'session_id' hat einen ungültigen Wert!")
            raise CorruptSessionError()

        session_key = f"{self._KEY_PREFIX}{session_id}"

        result = await self.client.expire(session_key, ttl_sec)

        return result
