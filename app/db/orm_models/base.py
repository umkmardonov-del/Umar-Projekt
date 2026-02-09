# --- Gemeinsame SQLAlchemy Base ---
# --- path: /app/db/orm_models/base.py ---

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):
    pass

