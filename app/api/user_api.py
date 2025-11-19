# --- API-Endpunkte für unser Projekt ---
# --- path: /app/api/user_api.py ---

from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import postgres_dep
from app.pydantic_models.user_models import CalculatorIn, CalculatorOut
from app.service.user_service import calculate_prices_service

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/user",tags=["user"])


@router.post("/calculator", response_model=list[CalculatorOut], summary="Anforderungen von Website erhalten.")
async def get_user_specifications(request: Request,
                                  department: str = Form(...),
                                  team_members: int = Form(...),
                                  device_type: str = Form(...),
                                  operating_system: str = Form(...),
                                  included_software: str = Form(...),
                                  session: AsyncSession = Depends(postgres_dep)
                                  ) -> list[CalculatorOut]:
    #try:
        usage_mode = "mobile" if device_type.lower() == "laptop" else "stationary"

        payload = CalculatorIn(department=department, team_members=team_members, usage_mode=usage_mode,
                               os=operating_system, included_software=included_software)

        dto = await calculate_prices_service(session, payload=payload)

        return dto

    #except ValueError:
        raise HTTPException(status_code=404, detail="Not Found")
    # Exception:
        raise HTTPException(status_code=503, detail="Service Unavailable")




@router.get("/home", summary="Landing Page")
async def home_api(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
