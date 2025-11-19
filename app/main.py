# --- Main Datei zum Ausführen des Programmes ---
# --- path: /app/main.py

from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from uvicorn import run

from app.api.admin_api import router as admin_router
from app.api.user_api import router as user_router
from app.core.lifespan import lifespan
from app.core.settings import settings


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(debug=True,
              title=settings.APP_NAME,
              version="1.0.0",
              openapi_url=f"{settings.API_PREFIX}/openapi.json",
              docs_url=f"{settings.API_PREFIX}/docs",
              redoc_url=f"{settings.API_PREFIX}/redoc",
              lifespan=lifespan)


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(admin_router)
app.include_router(user_router)


if __name__ == "__main__":
    run("app.main:app", host=settings.HOST_LOCAL, port=settings.PORT, reload=settings.RELOAD, log_level=settings.LOG_LEVEL.lower())
