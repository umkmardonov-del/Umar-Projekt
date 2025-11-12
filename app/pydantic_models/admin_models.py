# --- Pydantic-Models für api_admin.py ---
# --- path: /app/models/admin_models ---

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, field_validator, PositiveInt
from typing import Annotated, Literal, Union, List
from uuid import UUID


# ------- Eingabe-Schemata fürs Anlegen von Produkten -------

ProductString = Annotated[str, StringConstraints(min_length=1, max_length=200, strip_whitespace=True),
                               Field(..., description="Name des Produkts.")]

PriceString = Annotated[Decimal, Field(..., ge=0, max_digits=7, decimal_places=2,
                                       description="Preis des Produkts.",
                                       examples=["42,56", "100", "567.87"])]


class BaseProductIn(BaseModel):
    name: ProductString

    price: PriceString

    @field_validator("price", mode="before")
    @classmethod
    def _comma_to_point(cls, var):
        return var.replace(",", ".") if isinstance(var, str) else var

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class LaptopIn(BaseProductIn):
    type: Literal["laptop"]

    processor: str = Field(...,
                           max_length=50,
                           description="Prozessor als String, höchstens 50 Zeichen.")
    operating_system: str = Field(...,
                                  max_length=50,
                                  description="OS als String, höchstens 50 Zeichen.")
    memory: str = Field(...,
                        max_length=50,
                        description="Arbeitsspeicher als String, höchstens 50 Zeichen.")
    disc_memory: str = Field(...,
                             max_length=50,
                             description="Festplatte als String, höchstens 50 Zeichen.")
    screen_size: int = Field(...,
                             description="Bildschirmdiagonale als Zahl(wichtig)!")
    resolution_height: int = Field(...,
                                   description="Pixelhöhe als Zahl(wichtig)!")
    resolution_width: int = Field(...,
                                  description="Pixelbreite als Zahl(wichtig)!")
    refresh_rate: int = Field(...,
                              description="Bildschirmwiederholungsrate als Zahl(wichtig)!")
    graphics_card: str = Field(...,
                               max_length=100,
                               description="Grafikkarte als String, höchstens 100 Zeichen. Wenn leer: default='Integrierte Grafikkarte.'")
    camera: str = Field(...,
                        max_length=100,
                        description="Kamera als String, höchstens 100 Zeichen.")


class MonitorIn(BaseProductIn):
    type: Literal["monitor"]

    resolution_height: int = Field(...,
                                   description="Pixelhöhe als Zahl(wichtig)!")
    resolution_width: int = Field(...,
                                  description="Pixelbreite als Zahl(wichtig)!")
    latency: int = Field(...,
                         description="Latenz als Zahl(wichtig)!")
    refresh_rate: int = Field(...,
                              description="Bildschirmwiederholungsrate als Zahl(wichtig)!")
    power_usage: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Stromverbrauch als Zahl(Kommastellen erlaubt).",
                                 examples=["42,56", "100", 567.87])
    screen_size: int = Field(...,
                             description="Bildschirmdiagonale als Zahl(wichtig)!")
    connectors: str = Field(...,
                            max_length=200,
                            description="Anschlüsse als String, höchstens 200 Zeichen.")

    @field_validator("power_usage", mode="before")
    @classmethod
    def _comma_to_point(cls, var):
        return var.replace(",", ".") if isinstance(var, str) else var


class DeskIn(BaseProductIn):
    type: Literal["desk"]

    height_adjustable: bool = Field(...,
                                    description="Höhenverstellbar als bool: True oder False")
    dimensions: str = Field(...,
                            max_length=20,
                            description="Maße des Tisches, höchstens 20 Zeichen",
                            examples=["160x100", "1,6m x 1m"])
    description: str = Field(...,
                             max_length=200,
                             description="Sonstige Vorteile des Tisches, höchstens 200 Zeichen.")


ProductIn = Annotated[Union[LaptopIn, MonitorIn, DeskIn], Field(discriminator="type")]

# ------- Update-Schemata für Produkte -------

pass


# ------- Ausgabe-Schemata für Produkte -------

class BaseProductOut(BaseModel):
    id: UUID = Field(...,
                     description="Produkt-ID in der Datenbank, wird automatisch zugewiesen.")
    name: ProductString

    price: PriceString

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class LaptopOut(BaseProductOut):
    type: Literal["laptop"] = "laptop"

    processor: str = Field(...,
                           max_length=50,
                           description="Prozessor als String, höchstens 50 Zeichen.")
    operating_system: str = Field(...,
                                  max_length=50,
                                  description="OS als String, höchstens 50 Zeichen.")
    memory: str = Field(...,
                        max_length=50,
                        description="Arbeitsspeicher als String, höchstens 50 Zeichen.")
    disc_memory: str = Field(...,
                             max_length=50,
                             description="Festplatte als String, höchstens 50 Zeichen.")
    screen_size: int = Field(...,
                             description="Bildschirmdiagonale als Zahl(wichtig)!")
    resolution_height: int = Field(...,
                                   description="Pixelhöhe als Zahl(wichtig)!")
    resolution_width: int = Field(...,
                                  description="Pixelbreite als Zahl(wichtig)!")
    refresh_rate: int = Field(...,
                              description="Bildschirmwiederholungsrate als Zahl(wichtig)!")
    graphics_card: str = Field(...,
                               max_length=100,
                               description="Grafikkarte als String, höchstens 100 Zeichen. Wenn leer: default='Integrierte Grafikkarte.'")
    camera: str = Field(...,
                        max_length=100,
                        description="Kamera als String, höchstens 100 Zeichen.")


class MonitorOut(BaseProductOut):
    type: Literal["monitor"] = "monitor"

    resolution_height: int = Field(...,
                                   description="Pixelhöhe als Zahl(wichtig)!")
    resolution_width: int = Field(...,
                                  description="Pixelbreite als Zahl(wichtig)!")
    latency: int = Field(...,
                         description="Latenz als Zahl(wichtig)!")
    refresh_rate: int = Field(...,
                              description="Bildschirmwiederholungsrate als Zahl(wichtig)!")
    power_usage: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Stromverbrauch als Zahl(Kommastellen erlaubt).",
                                 examples=["42,56", "100", 567.87])
    screen_size: int = Field(...,
                             description="Bildschirmdiagonale als Zahl(wichtig)!")
    connectors: str = Field(...,
                            max_length=200,
                            description="Anschlüsse als String, höchstens 200 Zeichen.")


class DeskOut(BaseProductOut):
    type: Literal["desk"] = "desk"

    height_adjustable: bool = Field(...,
                                    description="Höhenverstellbar als Boolean.",
                                    examples=[True, False])
    dimensions: str = Field(...,
                            max_length=20,
                            description="Maße des Tisches, höchstens 20 Zeichen",
                            examples=["160x100", "1,6m x 1m"])
    description: str = Field(...,
                             max_length=200,
                             description="Sonstige Vorteile des Tisches, höchstens 200 Zeichen.")


ProductOut = Annotated[Union[LaptopOut, MonitorOut, DeskOut], Field(discriminator="type")]


# --- Paketklassen als ENUM ---

class Tier(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ULTRA = "ultra"


#------- Eingabe-Schemata für Pakete -------

class PackageItemIn(BaseModel):
    product_id: UUID = Field(...,
                             description="Datenbank Produkt-ID.")

    quantity: PositiveInt = Field(...,
                                  description="Produktmenge als positive Zahl(wichtig).")

    model_config = ConfigDict(extra="forbid")


class PackageIn(BaseModel):
    department_id: UUID = Field(...,
                                description="Datenbank Department-ID.")

    tier: Tier = Field(...,
                       description="'basic', 'premium' oder 'ultra'")

    items: List[PackageItemIn] = Field(default_factory=list,
                                          description="Inhalt des Paketes nach PackageItemIn-Schema.")

    model_config = ConfigDict(extra="forbid")


# ------- Ausgabeschemata für Pakete -------

class PackageItemOut(BaseModel):
    id: UUID = Field(...,
                    description="Datenbank PackageItem-ID.")

    quantity: PositiveInt = Field(...,
                                  description="Produktmenge als Zahl(wichtig).")

    product: ProductOut

    model_config = ConfigDict(from_attributes=True)


class PackageOut(BaseModel):
    id: UUID = Field(...,
                     description="Datenbank Paket-ID.")

    department_id: UUID = Field(...,
                                description="Datenbank Department-ID.")

    tier: Tier = Field(...,
                       description="'basic', 'premium' oder 'ultra'")

    items: List[PackageItemOut] = Field(default_factory=list,
                                        description="Inhalt des Paketes nach PackageItemIn-Schema.")

    model_config = ConfigDict(from_attributes=True)


# ------- Ein- und Ausgabeschema für Abteilungen -------

DepartmentString = Annotated[str, StringConstraints(min_length=1, max_length=100, strip_whitespace=True),
                                  Field(..., description="Einmalig vergebbarer Name der Abteilung, höchstens 100 Zeichen.")]


class DepartmentIn(BaseModel):
    name: DepartmentString

    model_config = ConfigDict(extra="forbid")


class DepartmentOut(BaseModel):
    id: UUID = Field(...,
                     description="Datenbank Department-ID.")

    name: DepartmentString

    packages: List[PackageOut] = Field(default_factory=list,
                                       description="Gibt Liste von Paketen aus, deren Inhalt Liste aus Produkten ist.")

    model_config = ConfigDict(from_attributes=True)
    