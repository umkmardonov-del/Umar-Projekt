# --- API "Admin" Endpunkte ---
# --- path: /app/api/admin_api.py ---

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.deps import postgres_dep
from app.pydantic_models.admin_models import ProductIn, ProductOut
from app.service.admin_service import create_product_service


router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/product", status_code=201, response_model=ProductIn, summary="Produkte anlegen.")
async def create_product_api(payload: ProductIn,
                             request: Request,
                             response: Response,
                             session: AsyncSession = Depends(postgres_dep),
                             ) -> ProductOut:
    try:
        dto = await create_product_service(session, payload)

        location = str(request.url_for("get_product_by_id", ident=dto.id))
        response.headers["Location"] = location

        return ProductOut(dto)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict")


@router.get("/product/{ident}", response_model=ProductOut, name="get_product_by_id",
            summary="Einzelnes Produkt anhand seiner ID abrufen.")
async def get_product_by_id(ident: UUID,
                            session: AsyncSession = Depends(postgres_dep)):
    pass
