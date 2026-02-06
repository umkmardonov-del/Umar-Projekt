# --- Authentifizierungslogik ---
# --- path: app/security/auth.py ---

from fastapi import Request, Response
from logging import getLogger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .session_data import SessionData, is_session_data
from .session_store import SessionStore
from app.db.orm_models.users import User
from app.core.exceptions import SessionTimeoutError, CorruptSessionError, NotPermittedError, NotAuthorizedError
from ..core.settings import settings

logger = getLogger(__name__)


async def get_auth_session(request: Request,
                           response: Response,
                           session: AsyncSession,
                           store: SessionStore) -> SessionData:

    session_id = request.cookies.get("session_id")

    if session_id is None or session_id.strip() == "":
        raise SessionTimeoutError()

    store_data = await store.get(session_id)

    if store_data is None:
        raise SessionTimeoutError()

    elif not is_session_data(store_data):
        logger.error("Falscher type() im store_data.")
        raise CorruptSessionError()

    session_data: SessionData = store_data

    active = await get_user_status(session, user_id=session_data["user_id"])
    if active is None:
        raise NotAuthorizedError()
    elif not active:
        raise NotPermittedError()

    if settings.SESSION_ROLLING:
        prolonged = await store.expire(session_id)
        if not prolonged:
            raise SessionTimeoutError()
        elif prolonged:
            response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                                value=session_id,
                                max_age=settings.SESSION_MAX_AGE_SEC,
                                expires=None,
                                path=settings.COOKIE_PATH,
                                domain=settings.COOKIE_DOMAIN,
                                secure=settings.COOKIE_SECURE,
                                httponly=True,
                                samesite=settings.COOKIE_SAMESITE)

    return session_data


# --- Helper Funktionen ---
async def get_user_status(session: AsyncSession, *, user_id: str) -> Optional[bool]:
    stmt = select(User.is_active).where(User.id == user_id)

    result = (await session.execute(stmt)).first()

    if result is None:
        return None
    else:
        return bool(result[0])
