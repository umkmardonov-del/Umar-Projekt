# --- API "Admin" Endpunkte ---
# --- path: /app/api/admin_api.py ---

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.deps import postgres_dep
from app.pydantic_models.admin_models import ProductIn, ProductOut, DepartmentOut, DepartmentIn, ProductListOut, \
    PackageOut, PackageIn
from app.service.admin_service import (create_product_service, get_product_by_id_service, create_department_service,
                                       get_department_by_id_service, get_all_products_service, delete_product_service,
                                       get_products_by_type_service, get_all_departments_service,
                                       create_package_service)

router = APIRouter(prefix="/admin", tags=["admin"])


# --- Produktspezifische Endpunkte ---

@router.post("/product", status_code=201, response_model=ProductOut, summary="Produkte anlegen.")
async def create_product_api(payload: ProductIn,
                             request: Request,
                             response: Response,
                             session: AsyncSession = Depends(postgres_dep),
                             ) -> ProductOut:
    try:
        dto = await create_product_service(session, payload=payload)

        location = str(request.url_for("get_product_by_id", ident=dto.id))
        response.headers["Location"] = location

        return dto

    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict")


@router.get("/products/{product_type}", response_model=list[ProductOut], summary="Alle Produkte eines bestimmten Typs abfragen.")
async def get_products_by_type_api(product_type: str,
                               session: AsyncSession = Depends(postgres_dep)
                               ) -> list[ProductOut]:
    try:
        products = await get_products_by_type_service(session, product_type)

        return products

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/product/{ident}", response_model=ProductOut, name="get_product_by_id",
            summary="Einzelnes Produkt anhand seiner ID abrufen.")
async def get_product_by_id_api(ident: UUID,
                                session: AsyncSession = Depends(postgres_dep),
                                ) -> ProductOut | None:
    try:
        dto = await get_product_by_id_service(session, ident=ident)

        return dto

    except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception:
        HTTPException(status_code=500, detail="Internal Error")


@router.get("/products", response_model=list[ProductListOut])
async def get_all_products_api(session: AsyncSession = Depends(postgres_dep)) -> list[ProductListOut]:
    try:
        dto = await get_all_products_service(session)

        return dto

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@router.delete("/product/{ident}", status_code=204)
async def delete_product_api(ident: UUID,
                             session: AsyncSession = Depends(postgres_dep),
                             ):
    try:
        await delete_product_service(session, ident=ident)

        return "erfolgreich"

    except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


# --- Abteilungsspezifische Endpunkte ---

@router.post("/department", status_code=201, response_model=DepartmentOut)
async def create_department_api(payload: DepartmentIn,
                                request: Request,
                                response: Response,
                                session: AsyncSession = Depends(postgres_dep)) -> DepartmentOut | None:
    try:
        dto = await create_department_service(session, payload=payload)

        location = str(request.url_for("get_department_by_id", ident=dto.id))
        response.headers["Location"] = location

        return dto

    except IntegrityError:
        raise HTTPException(status_code=509, detail="Conflict")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/department", response_model=list[DepartmentOut])
async def get_all_departments_api(session: AsyncSession = Depends(postgres_dep)):
    try:
        dto = await get_all_departments_service(session)

        return dto

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/department/{ident}", response_model=DepartmentOut, name="get_department_by_id",
            summary="Einzelne Abteilung anhand seiner ID abrufen.")
async def get_department_by_id_api(ident: UUID,
                                   session: AsyncSession = Depends(postgres_dep),
                                   ) -> DepartmentOut | None:
    try:
        dto = await get_department_by_id_service(session, ident=ident)

        return dto

    except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception:
        HTTPException(status_code=500, detail="Internal Error")


# --- Paketspezifische Endpunkte ---

@router.post("/package", status_code=201, response_model=PackageOut)
async def create_package_api(payload: PackageIn,
                             request: Request,
                             response : Response,
                             session: AsyncSession = Depends(postgres_dep)):
    try:
        dto = await create_package_service(session, payload=payload)

        location = str(request.url_for("get_department_by_id", ident=dto.id))
        response.headers["Location"] = location

        return dto

    except Exception:
        raise HTTPException(status_code=503, detail="Service Unavailable")


# --- Tests ---

@router.get("/test")
async def test_endpoint():
    return "erfolgreich"
