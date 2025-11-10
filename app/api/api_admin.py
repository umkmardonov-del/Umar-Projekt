# --- API "Admin" Endpunkte ---
# --- path: /app/api/api_admin.py ---
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import postgres_dep


router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/add", status_code=201)
async def create_database_entries(payload: dict,
                                  session: AsyncSession = Depends(postgres_dep)):
    pass