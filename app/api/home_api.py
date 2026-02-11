# --- Home Endpunkt ---
# --- path: app/api/home_api.py ---

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.security.permissions import PermissionHandler


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(tags=["home"])


@router.get("/", summary="Landing Page",
            dependencies=[])
async def home_api(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})
