# --- Pydantic-Models für API In- und Output ---
# --- path: /app/pydantic_models/user_models.py ---

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, PositiveInt
from typing import Annotated, Optional


# --- Enum(s) ---

class Tier(str, Enum):
    basic = "basic"
    premium = "premium"
    ultra = "ultra"


class UsageMode(str, Enum):
    mobile = "mobile"
    stationary = "stationary"


# --- Eingabeschema für Calculator ---

class CalculatorIn(BaseModel):
    department: str = Field(...,)
    team_members: PositiveInt = Field(...,)
    usage_mode: str = Field(...,
                                  description="'mobile' oder 'stationary'")
    os: str = Field(...,)
    included_software: str = Field(...,)

    model_config = ConfigDict(extra="forbid")


# --- Ausgabeschema für Calculator ---

DepartmentString = Annotated[str, StringConstraints(min_length=1, max_length=100, strip_whitespace=True),
                                  Field(..., description="Einmalig vergebbarer Name der Abteilung, höchstens 100 Zeichen.")]

ProductString = Annotated[str, StringConstraints(min_length=1, max_length=200, strip_whitespace=True),
                               Field(..., description="Name des Produkts.")]

PriceString = Annotated[Decimal, Field(..., ge=0, max_digits=9, decimal_places=2,
                                       description="Preis des Produkts.",
                                       examples=["42,56", "100", "567.87"])]


class CalculatorOut(BaseModel):
    department_name: DepartmentString
    tier: Tier = Field(...)
    usage_mode: UsageMode = Field(...)
    items: list[CalculatorItemOut] = Field()

    members: PositiveInt = Field(...)
    os: str = Field(...)
    include_software: str = Field(...)

    hardware_cost_member: PriceString
    hardware_cost_total: PriceString
    energy_cost_member: Decimal = Field(..., ge=0, max_digits=7, decimal_places=3,
                                       description="Energieverbrauch des Produkts.",
                                       examples=["42,56", "100", "567.87"])
    energy_cost_total: Decimal = Field(..., ge=0, max_digits=7, decimal_places=3,
                                       description="Energieverbrauch des Produkts.",
                                       examples=["42,56", "100", "567.87"])

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class CalculatorItemOut(BaseModel):
    product_name: ProductString
    price: PriceString
    power_usage: Optional[Decimal] = Field(default=None)

    model_config = ConfigDict(extra="forbid", from_attributes=True)
