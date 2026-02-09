# --- Auth-Repository für User ---
# --- path: /app/db/repositories/user_repository.py ---

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm_models.auth_orm import User, Permission, RolePermission, UserRole


async def register_user(session: AsyncSession, *,
                        name: str,
                        surname: str,
                        email: str,
                        pw_hash: str) -> User:
    new_user_orm = User(name=name,
                        surname=surname,
                        email=email,
                        pw_hash=pw_hash)

    session.add(new_user_orm)

    await session.flush()
    await session.refresh(new_user_orm)

    return new_user_orm


async def get_user_by_email(session: AsyncSession, *, email: str) -> Optional[User]:
    email = email.strip().lower()

    stmt = select(User).where(User.email == email)

    query = await session.execute(stmt)

    user = query.scalar_one_or_none()

    return user


async def get_permission_codes_by_id(session: AsyncSession, *, ident: UUID) -> list[str]:
    stmt = (select(Permission.code)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .where(UserRole.user_id == ident)
            .distinct()
            .order_by(Permission.code))

    result = await session.execute(stmt)

    return list(result.scalars().all())
