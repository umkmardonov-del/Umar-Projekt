from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import postgres_dep
from app.pydantic_models.user_models import CalculatorIn
from app.service.user_service import calculate_results_service

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(prefix="/user", tags=["user"])


# ✅ FIXED VERSION
@router.post("/calculator", response_class=HTMLResponse, summary="Calculator Endpoint")
async def get_user_specifications(
    request: Request,
    department: str = Form(...),
    team_members: int = Form(...),
    device_type: str = Form(...),
    operating_system: str = Form(...),
    included_software: str = Form(...),
    session: AsyncSession = Depends(postgres_dep)
):
    try:
        usage_mode = "mobile" if device_type.lower() == "laptop" else "stationary"

        payload = CalculatorIn(
            department=department,
            team_members=team_members,
            usage_mode=usage_mode,
            os=operating_system,
            included_software=included_software
        )

        dto = await calculate_results_service(session, payload=payload)

        # ✅ VERY IMPORTANT PART
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "dto": dto
            }
        )

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/home", response_class=HTMLResponse)
async def home_api(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ------- Template helper -------

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
