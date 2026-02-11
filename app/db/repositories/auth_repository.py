# --- Auth-Repository für User ---
# --- path: /app/db/repositories/auth_repository.py ---

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm_models.auth_orm import User, Role, Permission, RolePermission, UserRole
from app.pydantic_models.auth_models import RegisterIn


async def register_user(session: AsyncSession, *, payload: RegisterIn, email: str, pw_hash: str) -> User:

    new_user_orm = User(name=payload.name, surname=payload.surname, email=email, pw_hash=pw_hash)

    session.add(new_user_orm)

    await session.flush()
    await session.refresh(new_user_orm)

    return new_user_orm


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    email = email.strip().lower()

    stmt = select(User).where(User.email == email)

    query = await session.execute(stmt)

    user = query.scalar_one_or_none()

    return user


async def get_permission_codes_by_id(session: AsyncSession, ident: UUID) -> list[str]:
    stmt = (select(Permission.code)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .where(UserRole.user_id == ident)
            .distinct()
            .order_by(Permission.code))

    result = await session.execute(stmt)

    return list(result.scalars().all())


# --- Admin Funktionen --
async def create_role(session: AsyncSession, *, name: str, description: str) -> Role:

    new_role_orm = Role(name=name, description=description)

    session.add(new_role_orm)

    await session.flush()
    await session.refresh(new_role_orm)

    return new_role_orm


async def create_permission(session: AsyncSession, *, code: str, description: str) -> Permission:

    new_permission_orm = Permission(code=code, description=description)

    session.add(new_permission_orm)

    await session.flush()
    await session.refresh(new_permission_orm)

    return new_permission_orm


async def get_role_by_name(session: AsyncSession, name: str) -> Optional[Role]:

    stmt = select(Role).where(Role.name == name)

    result = (await session.execute(stmt)).scalar_one_or_none()

    return result


async def get_permission_by_code(session: AsyncSession, code: str) -> Optional[Permission]:

    stmt = select(Permission.code).where(Permission.code == code)

    result = (await session.execute(stmt)).scalar_one_or_none()

    return result


async def create_user_role(session: AsyncSession, *, user: User, role: Role) -> UserRole:

    new_user_role_orm = UserRole(user=user, role=role) # Ids werden automatisch verknüpft

    session.add(new_user_role_orm)

    await session.flush()
    await session.refresh(new_user_role_orm)

    return new_user_role_orm


async def create_role_permission(session: AsyncSession, *, role: Role,
                                 permission: Permission) -> RolePermission:

    new_role_permission_orm = RolePermission(role=role, permission=permission)

    session.add(new_role_permission_orm)

    await session.flush()
    await session.refresh(new_role_permission_orm)

    return new_role_permission_orm
