# --- Pydantic-Models für API In- und Output ---
# --- path: /app/pydantic_models/models.py ---

from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict, StringConstraints
from typing import Annotated


DepartmentList = Annotated[str, StringConstraints(min_length=1, max_length=200, strip_whitespace=True)]

class SpecsIn(BaseModel):
    department: DepartmentList = Field(...,
                            description="Name der Abteilung.",
                            examples=["HR", "IT", "Geschäftsführung"])
    member_count: int = Field(...,
                                    description="Anzahl Mitglieder in einer Abteilung als int.",
                                    examples=[1, 23, 100])
    mobile: bool = Field(...,
                         description="Ist mobile oder stationäre Ausstattung gesucht?",
                         examples=[True, False])

    model_config = ConfigDict(extra="forbid")
