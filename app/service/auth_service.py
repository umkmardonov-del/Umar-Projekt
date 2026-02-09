# --- Service Funktionen für User-Auth ---
# --- path: /app/service/auth/auth_service.py ---

from datetime import datetime
from fastapi import Request, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from zoneinfo import ZoneInfo

from app.core.settings import settings
from app.db.orm_models.auth_orm import User
from app.db.repositories.auth_repository import get_user_by_email, register_user, get_permission_codes_by_id
from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.pydantic_models.auth_models import RegisterIn, UserOut, LoginIn
from app.security.passwords import hash_password, needs_rehash, verify_password, generate_secret_token
from app.security.session_data import SessionData
from app.security.session_store import SessionStore


async def register_user_service(session: AsyncSession,
                                *,
                                payload: RegisterIn) -> User:

    name = payload.name.strip()
    surname = payload.surname.strip()
    email = payload.email
    password = payload.password.get_secret_value()

    assigned = await get_user_by_email(session, email=email)
    if assigned:
        raise EmailAlreadyRegisteredError()

    pw_hash = hash_password(password)

    try:
        user = await register_user(session, name=name, surname=surname, email=email, pw_hash=pw_hash)

    except IntegrityError:
        raise EmailAlreadyRegisteredError()

    return user


async def login_user_service(session: AsyncSession,
                             *,
                             payload: LoginIn) -> User:

    user_dto = await get_user_by_email(session, email=payload.email)
    if not user_dto:
        raise InvalidCredentialsError()

    password = payload.password.get_secret_value()

    authenticated = verify_password(password, user_dto.pw_hash)
    if not authenticated:
        raise InvalidCredentialsError()

    if needs_rehash(user_dto.pw_hash) and authenticated:
        new_pw_hash = hash_password(password)

        user_dto.pw_hash = new_pw_hash

        session.add(user_dto.pw_hash)

        await session.flush()
        await session.refresh(user_dto)

    return user_dto


async def create_auth_session_service(session: AsyncSession,
                                      store: SessionStore,
                                      *,
                                      response: Response,
                                      user: User) -> UserOut:

    data: SessionData = {"user_id": str(user.id),
                         "issued_at": int(datetime.now(tz=ZoneInfo("Europe/Berlin")).timestamp()),
                         "permissions": await get_permission_codes_by_id(session, ident=user.id)}

    await session.commit()

    session_id = generate_secret_token()

    await store.login_user(session_id, data)

    response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                        value=session_id,
                        max_age=settings.SESSION_MAX_AGE_SEC,
                        expires=None,
                        path=settings.COOKIE_PATH,
                        domain=settings.COOKIE_DOMAIN,
                        secure=settings.COOKIE_SECURE,
                        httponly=True,
                        samesite=settings.COOKIE_SAMESITE)

    user_dto = UserOut.model_validate(user)

    return user_dto


async def logout_user_service(store: SessionStore,
                              data: SessionData,
                              *,
                              request: Request,
                              response: Response) -> None:

    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    user_id = data["user_id"]

    await store.logout_user(session_id, user_id)

    invalidate_cookies(response, session_id)


# --- Helper ---
def invalidate_cookies(response: Response, session_id: str) -> None:

    response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                        value=session_id,
                        max_age=0,
                        expires=None,
                        path=settings.COOKIE_PATH,
                        domain=settings.COOKIE_DOMAIN,
                        secure=settings.COOKIE_SECURE,
                        httponly=True,
                        samesite=settings.COOKIE_SAMESITE)
