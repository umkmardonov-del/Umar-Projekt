# --- Pydantic-Models für api_admin.py ---
# --- path: /app/models/admin_models ---

from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict, StringConstraints, StrictInt, StrictBool, field_validator
from typing import Annotated, Literal


class DatabaseIn(BaseModel):
    tablename: Literal["Laptop", "PC",] = Field(...,
                                         description="Datenbankname",
                                         examples=["Laptop"])
