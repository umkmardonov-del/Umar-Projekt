# --- DB-Aufrufe für user Schicht ---
# --- path: /app/db/repositories/user_repository.py ---

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.orm_models.products import Department, PackageItem, Package


async def get_department_by_name(session: AsyncSession, department_name: str) -> Department | None:
    stmt = (select(Department)
            .options(selectinload(Department.packages).
                     selectinload(Package.items).
                     selectinload(PackageItem.product))
            .where(Department.name == department_name))

    query = await session.execute(stmt)

    department_orm = query.scalars().first()

    return department_orm
