# --- API-Endpunkte für unser Projekt ---
# --- path: /app/api/user_api.py ---

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import postgres_dep
from app.pydantic_models.user_models import SpecsIn


router = APIRouter(prefix="/user",tags=["user"])

@router.post("/", summary="Anforderungen von Website erhalten.")
async def get_user_specifications(payload: SpecsIn,
                                  session: AsyncSession = Depends(postgres_dep)):
    pass
