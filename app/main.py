# --- Main Datei zum Ausführen des Programmes ---
# --- path: /app/main.py ---

from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run

from app.api.auth_api import user_router as auth_user_router, admin_router as auth_admin_router
from app.api.products_api import admin_router as product_admin_router, user_router as product_user_router
from app.core.lifespan import lifespan
from app.core.logging_config import configure_logging
from app.core.settings import settings
from app.core.lifespan import lifespan
from app.service.admin_service import admin_router
from app.service.user_service import user_router


# ==========================================================
# BASE DIR
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

configure_logging()

app = FastAPI(
    debug=True,
    title=settings.APP_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    lifespan=lifespan
)


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# --- Product Routers ---
app.include_router(product_user_router)
app.include_router(product_admin_router)

# --- Auth Routers ---
app.include_router(auth_user_router)
app.include_router(auth_admin_router)


if __name__ == "__main__":
    run(
        "app.main:app",
        host=settings.HOST_LOCAL,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

