# --- Service-Funktionen für admin_api.py ---
# --- path: /app/service/admin_service.py ---

from __future__ import annotations

from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.repositories.product.admin_repository import (create_product, get_product_by_id, create_department,
                                                          get_department_by_id,
                                                          get_all_products, delete_product, get_products_by_type,
                                                          get_all_departments, create_package, get_all_packages)
from app.pydantic_models.product.admin_models import ProductIn, ProductOut, DepartmentIn, DepartmentOut, ProductListOut, PackageIn, PackageOut


# --- create_*-Funktionen ---

async def create_product_service(session:AsyncSession, *, payload: ProductIn) -> ProductOut:
    product_orm = await create_product(session, payload=payload)

    await session.commit()

    dto = TypeAdapter(ProductOut).validate_python(product_orm)

    return dto


async def create_department_service(session: AsyncSession, *, payload: DepartmentIn):
    department_orm = await create_department(session, payload=payload)

    await session.commit()

    dto = TypeAdapter(DepartmentOut).validate_python(department_orm)

    return dto


async def create_package_service(session: AsyncSession, payload: PackageIn):
    package_orm = await create_package(session, payload=payload)

    await session.commit()

    for item in package_orm.items:
        await session.refresh(item)

    dto = PackageOut.model_validate(package_orm)

    return dto


# --- get_all_*-Funktionen ---

async def get_all_products_service(session: AsyncSession) -> list[ProductListOut]:
    product_orm = await get_all_products(session)

    dto_items = [ProductListOut.model_validate(t) for t in product_orm]

    return dto_items


async def get_all_departments_service(session: AsyncSession) -> list[DepartmentOut]:
    department_orm = await get_all_departments(session)

    dto_items = [DepartmentOut.model_validate(t) for t in department_orm]

    return dto_items


async def get_all_packages_service(session: AsyncSession) -> list[PackageOut]:
    package_orm = await get_all_packages(session)

    for pkg in package_orm:
        for item in pkg.items:
            await session.refresh(item.product)

    dto = [PackageOut.model_validate(pkg) for pkg in package_orm]

    return dto


# --- get_*_by_id-Funktionen ---

async def get_product_by_id_service(session: AsyncSession, *, ident: UUID) -> ProductOut:
    product_orm = await get_product_by_id(session, product_id=ident)
    if not product_orm:
        raise ValueError("Produkt nicht gefunden.")

    await session.refresh(product_orm)

    dto = TypeAdapter(ProductOut).validate_python(product_orm)

    return dto


async def get_department_by_id_service(session: AsyncSession, *, ident: UUID) -> DepartmentOut:
    department_orm = await get_department_by_id(session, department_id=ident)
    if not department_orm:
        raise ValueError("Abteilung nicht gefunden.")

    await session.refresh(department_orm)

    dto = DepartmentOut.model_validate(department_orm)

    return dto


# --- Produkte nach Typ ---

async def get_products_by_type_service(session: AsyncSession, product_type: str) -> list[ProductOut]:
    products_orm = await get_products_by_type(session, product_type)

    dto_items = [TypeAdapter(ProductOut).validate_python(t) for t in products_orm]

    return dto_items


# --- delete_*-Funktionen ---

async def delete_product_service(session: AsyncSession, *, ident: UUID) -> None:
    deleted = await delete_product(session, product_id=ident)
    if not deleted:
        raise ValueError("Produkt nicht gefunden.")

    await session.commit()

    return None
