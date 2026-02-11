# --- Main Datei zum Ausführen des Programmes ---
# --- path: /app/main.py ---

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from uvicorn import run

from app.api.auth_api import user_router as auth_user_router, admin_router as auth_admin_router
from app.api.home_api import router as home_router
from app.api.products_api import admin_router as product_admin_router, user_router as product_user_router
from app.core.logging_config import configure_logging
from app.core.settings import settings
from app.core.lifespan import lifespan


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


# --- Home Router ---
app.include_router(home_router)

# --- Product Routers ---
app.include_router(product_user_router)
app.include_router(product_admin_router)

# --- Auth Routers ---
app.include_router(auth_user_router)
app.include_router(auth_admin_router)


if __name__ == "__main__":
    run("app.main:app",
        host=settings.HOST_LOCAL,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower())
