# --- Authentifizierungslogik ---
# --- path: app/security/auth.py ---

from fastapi import Request, Response, Depends
from logging import getLogger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.security.session_data import SessionData, is_session_data
from app.security.session_store import SessionStore
from app.db.orm_models.auth_orm import User
from app.core.exceptions import SessionTimeoutError, CorruptSessionError, NotPermittedError, NotAuthorizedError
from app.core.settings import settings

logger = getLogger(__name__)


async def get_auth_session(session: AsyncSession,
                           store: SessionStore,
                           *,
                           request: Request,
                           response: Response) -> SessionData:

    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)

    if session_id is None or session_id.strip() == "":
        raise SessionTimeoutError()

    store_data = await store.get(session_id)

    if not is_session_data(store_data):
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
