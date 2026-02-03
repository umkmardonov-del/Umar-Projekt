# --- Main Datei zum Ausführen des Programmes ---
# --- path: /app/main.py ---

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.api.admin_api import router as admin_router
from app.api.user_api import router as user_router
from app.core.lifespan import lifespan
from app.core.settings import settings

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    debug=True,
    title=settings.APP_NAME,
    version="1.0.0",
    # WICHTIG: docs ohne Prefix erreichbar machen
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Static Files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# API Router
app.include_router(admin_router)
app.include_router(user_router)

# Frontend
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", include_in_schema=False)
async def results(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})
