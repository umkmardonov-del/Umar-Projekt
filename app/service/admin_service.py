# --- Service-Funktionen für admin_api.py ---
# --- path: /app/service/admin_service.py ---

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.repositories.admin_repository import create_product, get_product_by_id
from app.pydantic_models.admin_models import ProductIn, ProductOut


# --- create_*-Funktionen ---

async def create_product_service(session:AsyncSession, payload: ProductIn) -> ProductOut:
    product_orm = await create_product(session, payload)

    await session.commit()

    dto = ProductOut.model_validate(product_orm)

    return dto


# --- get_*_by_id-Funktionen ---

async def get_product_by_id_service(session: AsyncSession, ident: UUID) -> ProductOut:
    product_orm = await get_product_by_id(session, ident)
    if not product_orm:
        raise ValueError("Produkt nicht gefunden.")

    dto = ProductOut.model_validate(product_orm)

    return dto
