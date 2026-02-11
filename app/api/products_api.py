# --- Admin- und User-Endpunkte für product_api.py ---
# --- path: /app/api/product_api.py ---

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.deps import postgres_dep, auth_session_dep
from app.pydantic_models.product.admin_models import ProductIn, ProductOut, DepartmentOut, DepartmentIn, ProductListOut, \
    PackageOut, PackageIn
from app.security.permissions import PermissionHandler
from app.service.product.admin_service import (create_product_service, get_product_by_id_service,
                                               create_department_service,
                                               get_department_by_id_service, get_all_products_service,
                                               delete_product_service,
                                               get_products_by_type_service, get_all_departments_service,
                                               create_package_service, get_all_packages_service)

admin_router = APIRouter(prefix="/product/admin", tags=["admin", "product"])


# ------- Admin-Routen -------
# --- Produktspezifische Endpunkte ---

@admin_router.post("/product", status_code=201, response_model=ProductOut, summary="Produkte anlegen.")
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


@admin_router.get("/products/{product_type}", response_model=list[ProductOut],
                  summary="Alle Produkte eines bestimmten Typs abfragen.")
async def get_products_by_type_api(product_type: str,
                                   session: AsyncSession = Depends(postgres_dep)
                                   ) -> list[ProductOut]:
    try:
        products = await get_products_by_type_service(session, product_type)

        return products

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@admin_router.get("/product/{ident}", response_model=ProductOut, name="get_product_by_id",
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


@admin_router.get("", response_model=list[ProductListOut])
async def get_all_products_api(session: AsyncSession = Depends(postgres_dep)) -> list[ProductListOut]:
    try:
        dto = await get_all_products_service(session)

        return dto

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@admin_router.delete("/product/{ident}", status_code=204)
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

@admin_router.post("/department", status_code=201, response_model=DepartmentOut)
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
        raise HTTPException(status_code=409, detail="Conflict")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@admin_router.get("/departments", response_model=list[DepartmentOut])
async def get_all_departments_api(session: AsyncSession = Depends(postgres_dep)):
    try:
        dto = await get_all_departments_service(session)

        return dto

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Error")


@admin_router.get("/department/{ident}", response_model=DepartmentOut, name="get_department_by_id",
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

@admin_router.post("/package", status_code=201, response_model=PackageOut)
async def create_package_api(payload: PackageIn,
                             request: Request,
                             response: Response,
                             session: AsyncSession = Depends(postgres_dep)):
    try:
        dto = await create_package_service(session, payload=payload)

        location = str(request.url_for("get_department_by_id", ident=dto.id))
        response.headers["Location"] = location

        return dto

    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict")
    except Exception:
        raise HTTPException(status_code=503, detail="Service Unavailable")


@admin_router.get("/packages", response_model=list[PackageOut])
async def get_all_packages_api(session: AsyncSession = Depends(postgres_dep)
                               ) -> list[PackageOut]:
    try:
        dto = await get_all_packages_service(session)

        return dto

    except Exception:
        raise HTTPException(status_code=503, detail="Service Unavailable")


# --- Tests ---

@admin_router.get("/test", dependencies=[Depends(PermissionHandler(["user"], ["read"]))])
async def test_endpoint():
    return "erfolgreich"


# ------- User-Routen -------

from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import postgres_dep
from app.pydantic_models.product.user_models import CalculatorIn, CalculatorOut
from app.service.product.user_service import calculate_results_service

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

user_router = APIRouter(prefix="/product/user", tags=["user", "product"])


@user_router.post("/calculator", response_class=HTMLResponse, response_model=list[CalculatorOut],
                  response_model_exclude_none=True, summary="Anforderungen von Website erhalten.",
                  dependencies=[Depends(auth_session_dep)])
async def get_user_specifications(request: Request,
                                  department: str = Form(...),
                                  team_members: int = Form(...),
                                  device_type: str = Form(...),
                                  operating_system: str = Form(...),
                                  included_software: str = Form(...),
                                  session: AsyncSession = Depends(postgres_dep)
                                  ) -> HTMLResponse:
    try:
        usage_mode = "mobile" if device_type.lower() == "laptop" else "stationary"

        payload = CalculatorIn(department=department, team_members=team_members, usage_mode=usage_mode,
                               os=operating_system, included_software=included_software)

        dto = await calculate_results_service(session, payload=payload)

        return templates.TemplateResponse("results.html",
                                          {"request": request,
                                           "dto": dto})

    except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")
    except Exception:
        raise HTTPException(status_code=503, detail="Service Unavailable")


@user_router.get("/home", summary="Landing Page")
async def home_api(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


# ------- Helper -------

def trim_zeros(value, decimals: int | None = None) -> str:
    if value is None:
        return ""
    if decimals is not None:
        fmt = f"{{:.{decimals}f}}"
        s = fmt.format(float(value))
    else:
        s = str(value)

    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


templates.env.filters["trim_zeros"] = trim_zeros
