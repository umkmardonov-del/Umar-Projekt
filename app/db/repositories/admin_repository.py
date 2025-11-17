# --- DB-Aufrufe für admin Schicht ---
# --- path: /app/db/repositories/admin_repository.py ---

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import with_polymorphic, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
from uuid import UUID

from app.db.orm_models import (Product, Department, Package, PackageItem,
                               Laptop, Monitor, Desk, Workstation, Keyboard, Chair)
from app.pydantic_models.admin_models import BaseProductIn


# --- TYPE-MAP für Sortierung in ORM-Subklassen ---

TYPE_MAP: dict[str, Type[Product]] = {
    "laptop": Laptop,
    "monitor": Monitor,
    "desk": Desk,
    "workstation": Workstation,
    "chair": Chair,
    "keyboard" : Keyboard,
    "mouse": Mouse,
    "docking_station": DockingStation,
    "webcam": Webcam,
    "cable": Cable,
}



# --- create_*-Funktionen ---

async def create_product(session: AsyncSession, payload: BaseProductIn) -> Product:
    data = payload.model_dump()
    product_type = data.pop("product_type")

    base = {k: data.pop(k) for k in ("name", "price")}
    Model = TYPE_MAP[product_type]
    model = Model(**base, **data)

    session.add(model)

    try:
        await session.flush()
        await session.refresh(model)
    except IntegrityError as e:
        raise e

    return model


async def create_department(session: AsyncSession, *, payload: DepartmentIn) -> Department:
    data = payload.model_dump()
    name = data["name"]

    department_orm = Department(name=name)

    session.add(department_orm)

    try:
        await session.flush()
        await session.refresh(department_orm)

    except IntegrityError as e:
        raise e

    return department_orm


# --- get_all_*-Funktionen ---

async def get_all_products(session: AsyncSession) -> list[Product]:
    stmt = (select(Product)
            .options(selectinload(Product.package_items))
            .order_by(Product.product_type)
            )

    query = await session.execute(stmt)

    products_orm: list[Product] = list(query.scalars().all())

    return products_orm


# --- get_*_by_id-Funktionen ---

async def get_product_by_id(session: AsyncSession, product_id: UUID) -> Product | None:
    product_orm = await session.get(Product, product_id)

    return product_orm


async def get_package_by_id(session: AsyncSession, package_id: UUID) -> Package | None:
    package_orm = await session.get(Package, package_id)

    return package_orm


async def get_department_by_id(session: AsyncSession, department_id: UUID) -> Department | None:
    department_orm = await session.get(Department, department_id)

    return department_orm


async def get_packageitem_by_id(session: AsyncSession, packageitem_id: UUID) -> PackageItem | None:
    packageitem_orm = await session.get(PackageItem, packageitem_id)

    return packageitem_orm


# --- Produkte nach Typ ---

async def get_products_by_type(session: AsyncSession, product_type: str) -> list[Product]:
    if product_type not in TYPE_MAP:
        raise ValueError("Ungültiger product_type.")

    Model = TYPE_MAP[product_type]

    stmt = (select(Model)
            .options(selectinload(Model.package_items))
            .order_by(Model.name)
            )

    query = await session.execute(stmt)

    products_orm: list[Product] = list(query.scalars().all())

    return products_orm


# --- delete_*-Funktionen ---

async def delete_product(session, *, product_id) -> bool:
    product = await get_product_by_id(session, product_id=product_id)
    if not product:
        return False


    await session.delete(product)
    await session.flush()

    return True
