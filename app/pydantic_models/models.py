# --- Pydantic-Models für API In- und Output ---
# --- path: /app/pydantic_models/models.py ---

from __future__ import annotations

from pydantic import BaseModel, RootModel, Field, ConfigDict, StringConstraints, StrictInt, StrictBool, field_validator
from typing import Annotated


# --- Eingabeschema für Info-Sammel-Seite ---

DepartmentList = Annotated[str, StringConstraints(min_length=1, max_length=64, strip_whitespace=True)]

class InformationContents(BaseModel):
    department: DepartmentList = Field(...,
                            description="Name der Abteilung, mindestens 1 und höchstens 64 Zeichen.",
                            examples=["HR", "IT", "Geschäftsführung"])
    member_count: StrictInt = Field(...,
                                    ge=0,
                                    description="Anzahl Mitglieder in einer Abteilung als int.",
                                    examples=[1, 23, 100])
    mobile: StrictBool = Field(...,
                         description="Ist mobile oder stationäre Ausstattung gesucht?",
                         examples=[True, False])

    @field_validator("department")
    @classmethod
    def _no_empty_department(cls, validate: str):
        if not validate.strip():
            return ValueError("Feld 'Abteilung' darf nicht leer sein.")
        return validate

    model_config = ConfigDict(extra="forbid")


class InformationIn(RootModel[list[InformationContents]]):
    pass


# --- Eingabeschema für Spezifikationen ---

