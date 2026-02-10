from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run

from app.core.settings import settings
from app.core.lifespan import lifespan
from app.service.admin_service import admin_router
from app.service.user_service import user_router


# ==========================================================
# BASE DIR
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent


# ==========================================================
# APP INIT
# ==========================================================

app = FastAPI(
    debug=True,
    title=settings.APP_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    lifespan=lifespan
)


# ==========================================================
# STATIC FILES
# ==========================================================

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


# ==========================================================
# TEMPLATES
# ==========================================================

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ==========================================================
# ROOT ROUTE (FIX FOR 404)
# ==========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ==========================================================
# ROUTERS (DEINE BESTEHENDEN ROUTER)
# ==========================================================

app.include_router(admin_router)
app.include_router(user_router)


# ==========================================================
# LOCAL RUN
# ==========================================================

if __name__ == "__main__":
    run(
        "app.main:app",
        host=settings.HOST_LOCAL,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

