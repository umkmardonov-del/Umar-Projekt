# --- Service Funktionen für User-Auth ---
# --- path: /app/service/auth/auth_service.py ---

from datetime import datetime
from fastapi import Request, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import cast
from zoneinfo import ZoneInfo

from app.core.settings import settings
from app.db.orm_models.auth_orm import User
from app.db.repositories.auth_repository import (get_user_by_email, register_user, get_permission_codes_by_id,
                                                 create_role, get_role_by_name, get_permission_by_code,
                                                 create_permission, create_user_role, create_role_permission)
from app.core.exceptions import (EmailAlreadyRegisteredError, InvalidCredentialsError, RoleAlreadyExistsError,
                                 PermissionAlreadyExistsError)
from app.pydantic_models.auth_models import (RegisterIn, UserOut, LoginIn, RoleIn, RoleOut, PermissionIn, PermissionOut,
                                             RolePermissionIn, UserRoleIn, UserRoleOut, RolePermissionOut)
from app.security.passwords import hash_password, needs_rehash, verify_password, generate_secret_token
from app.security.session_data import SessionData
from app.security.session_store import SessionStore


# --- User Funktionen ---
async def register_user_service(session: AsyncSession, *, payload: RegisterIn) -> User:

    password = payload.password.get_secret_value()
    email = payload.email

    # --- Typechecker ---
    email = cast(object, email)
    email = cast(str, email)

    exists = await get_user_by_email(session, email=email)
    if exists:
        raise EmailAlreadyRegisteredError()

    pw_hash = hash_password(password)

    try:
        user = await register_user(session, payload=payload, email=email, pw_hash=pw_hash)

    except IntegrityError:
        raise EmailAlreadyRegisteredError()

    # --- Default-Rolle an neue User geben ---
    await create_user_role(session, user=user, role=settings.DEFAULT_ROLE)

    return user


async def login_user_service(session: AsyncSession, *, payload: LoginIn) -> User:

    email = payload.email

    # --- Typechecker ---
    email = cast(object, email)
    email = cast(str, email)

    user_dto = await get_user_by_email(session, email=email)
    if not user_dto:
        raise InvalidCredentialsError()

    password = payload.password.get_secret_value()

    authenticated = verify_password(password, user_dto.pw_hash)
    if not authenticated:
        raise InvalidCredentialsError()

    if needs_rehash(user_dto.pw_hash) and authenticated:
        new_pw_hash = hash_password(password)

        user_dto.pw_hash = new_pw_hash

        await session.flush()
        await session.refresh(user_dto)

    return user_dto


async def create_auth_session_service(session: AsyncSession, store: SessionStore,
                                      *, response: Response, user_orm: User) -> UserOut:

    data: SessionData = {"user_id": str(user_orm.id),
                         "issued_at": int(datetime.now(tz=ZoneInfo("Europe/Berlin")).timestamp()),
                         "permissions": await get_permission_codes_by_id(session, ident=user_orm.id)}

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

    user_dto = UserOut.model_validate(user_orm)

    return user_dto


async def logout_user_service(store: SessionStore, data: SessionData,
                              *, request: Request, response: Response) -> None:

    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    user_id = data["user_id"]

    await store.logout_user(session_id, user_id)

    invalidate_cookies(response, session_id)


# --- Admin Funktionen ---
async def create_role_service(session: AsyncSession, payload: RoleIn) -> RoleOut:

    name = payload.name
    description = payload.description

    exists = await get_role_by_name(session, name)
    if exists:
        raise RoleAlreadyExistsError()

    new_role_orm = await create_role(session, name=name, description=description)

    await session.commit()

    role_dto = RoleOut.model_validate(new_role_orm)

    return role_dto


async def create_permission_service(session: AsyncSession, payload: PermissionIn) -> PermissionOut:

    code = payload.code
    description = payload.description

    exists = await get_permission_by_code(session, code)
    if exists:
        raise PermissionAlreadyExistsError()

    new_permission_orm = await create_permission(session, code=code, description=description)

    await session.commit()

    permission_dto = PermissionOut.model_validate(new_permission_orm)

    return permission_dto


async def create_user_role_service(session: AsyncSession, payload: UserRoleIn) -> UserRoleOut:

    email = payload.email
    name = payload.role_name

    # --- Typechecker ---
    email = cast(object, email)
    email = cast(str, email)

    user = await get_user_by_email(session, email)
    role = await get_role_by_name(session, name)

    new_user_role_orm = await create_user_role(session, user=user, role=role)

    await session.commit()

    user_role_dto = UserRoleOut.model_validate(new_user_role_orm)

    return user_role_dto


async def create_role_permission_service(session: AsyncSession, payload: RolePermissionIn) -> RolePermissionOut:

    name = payload.role_name
    code = payload.permission_code

    role = await get_role_by_name(session, name)
    permission = await get_permission_by_code(session, code)

    new_role_permission_orm = await create_role_permission(session, role=role, permission=permission)

    await session.commit()

    role_permission_dto = RolePermissionOut.model_validate(new_role_permission_orm)

    return role_permission_dto


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
