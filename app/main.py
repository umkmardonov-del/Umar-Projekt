# --- Main Datei zum Ausführen des Programmes ---
# --- path: /app/main.py

from __future__ import annotations

from fastapi import FastAPI
from uvicorn import run

from app.core.lifespan import lifespan
from app.core.settings import settings

app = FastAPI(debug=True,
              title=settings.APP_NAME,
              version="1.0.0",
              openapi_url=f"{settings.API_PREFIX}/openapi.json",
              docs_url=f"{settings.API_PREFIX}/docs",
              redoc_url=f"{settings.API_PREFIX}/redoc",
              lifespan=lifespan)

if __name__ == "__main__":
    run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD, log_level=settings.LOG_LEVEL.lower())
