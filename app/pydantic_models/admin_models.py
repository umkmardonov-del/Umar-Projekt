# --- Pydantic-Models für admin_api.py ---
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

    model_config = ConfigDict(extra="forbid")


class LaptopIn(BaseProductIn):
    product_type: Literal["laptop"]

    processor: str = Field(...,
                           max_length=50,
                           description="Prozessor als String, höchstens 50 Zeichen.")
    operating_system: str = Field(...,
                                  max_length=50,
                                  description="OS als String, höchstens 50 Zeichen.")
    memory: str = Field(...,
                        max_length=50,
                        description="Arbeitsspeicher als String, höchstens 50 Zeichen.")
    power_usage: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Stromverbrauch als Zahl(Kommastellen erlaubt).",
                                 examples=["42,56", "100", 567.87])
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
    product_type: Literal["monitor"]

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
    product_type: Literal["desk"]

    height_adjustable: bool = Field(...,
                                    description="Höhenverstellbar als bool: True oder False")
    dimensions: str = Field(...,
                            max_length=20,
                            description="Maße des Tisches, höchstens 20 Zeichen",
                            examples=["160x100", "1,6m x 1m"])
    description: str = Field(...,
                             max_length=200,
                             description="Sonstige Vorteile des Tisches, höchstens 200 Zeichen.")


class WorkstationIn(BaseProductIn):
    product_type: Literal["workstation"]

    processor: str = Field(...,
                           max_length=50,
                           description="Prozessor als String, höchstens 50 Zeichen.")
    operating_system: str = Field(...,
                                  max_length=50,
                                  description="OS als String, höchstens 50 Zeichen.")
    memory: str = Field(...,
                        max_length=50,
                        description="Arbeitsspeicher als String, höchstens 50 Zeichen.")
    power_usage: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Stromverbrauch als Zahl(Kommastellen erlaubt).",
                                 examples=["42,56", "100", 567.87])
    disc_memory: str = Field(...,
                             max_length=50,
                             description="Festplatte als String, höchstens 50 Zeichen.")
    screen_size: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Bildschirmdiagonale als Zahl(wichtig)!",
                                 examples=["42,56", "100", 567.87])
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

class ChairIn(BaseProductIn):
    product_type: Literal["chair"]

    height_min: int = Field(..., )
    height_max: int = Field(..., )
    max_weight: PositiveInt = Field(..., )
    description: str = Field(...,
                             max_length=200,
                             description="Sonstige Vorteile des Stuhls, höchstens 200 Zeichen.")


class KeyboardIn(BaseProductIn):
    product_type: Literal["keyboard"]

    connection_style: str = Field(..., )
    layout: str = Field(..., )
    weight: PositiveInt = Field(..., )
    dimensions: str = Field(..., )
    description: str = Field(...,
                             max_length=200,
                             description="Sonstige Vorteile der Tastatur, höchstens 200 Zeichen.")


class MouseIn(BaseProductIn):
    product_type: Literal["mouse"]

    dpi: int = Field(..., )
    connection_style: str = Field(...,
                                  max_length=50)
    weight: int = Field(..., )
    battery: str = Field(...,
                             max_length=50)
    description: str = Field(...,
                                  max_length=200)


class DockingStationIn(BaseProductIn):
    product_type: Literal["docking_station"]

    display_port: int = Field(..., )
    hdmi: int = Field(..., )
    usb: str = Field(...,
                     max_length=80)
    usb_c: int = Field(..., )
    thunderbolt: int = Field(..., )
    ethernet: int = Field(..., )
    audio: int = Field(..., )



class WebcamIn(BaseProductIn):
    product_type: Literal["webcam"]

    fps: int = Field(..., )
    resolution: str = Field(...,
                            max_length=30)
    dfov_adjustable: bool = Field(..., )
    connection_style: str = Field(...,
                                  max_length=50)
    description: str = Field(...,
                             max_length=200)


class CableIn(BaseProductIn):
    product_type: Literal["cable"]

    hdmi: str = Field(...,
                      max_length=80)
    ethernet: str = Field(...,
                          max_length=80)
    usb_c: str = Field(...,
                       max_length=80)
    display_port: str = Field(...,
                              max_length=80)


ProductIn = Annotated[Union[
    LaptopIn, MonitorIn, DeskIn, WorkstationIn, ChairIn, KeyboardIn, MouseIn, DockingStationIn, WebcamIn, CableIn],
            Field(discriminator="product_type")]


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
    product_type: Literal["laptop"] = "laptop"

    processor: str = Field(...,
                           max_length=50,
                           description="Prozessor als String, höchstens 50 Zeichen.")
    operating_system: str = Field(...,
                                  max_length=50,
                                  description="OS als String, höchstens 50 Zeichen.")
    memory: str = Field(...,
                        max_length=50,
                        description="Arbeitsspeicher als String, höchstens 50 Zeichen.")
    power_usage: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Stromverbrauch als Zahl(Kommastellen erlaubt).",
                                 examples=["42,56", "100", 567.87])
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
    product_type: Literal["monitor"] = "monitor"

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
    product_type: Literal["desk"] = "desk"

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


class WorkstationOut(BaseProductOut):
    product_type: Literal["workstation"] = "workstation"

    processor: str = Field(...,
                           max_length=50,
                           description="Prozessor als String, höchstens 50 Zeichen.")
    operating_system: str = Field(...,
                                  max_length=50,
                                  description="OS als String, höchstens 50 Zeichen.")
    memory: str = Field(...,
                        max_length=50,
                        description="Arbeitsspeicher als String, höchstens 50 Zeichen.")
    power_usage: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Stromverbrauch als Zahl(Kommastellen erlaubt).",
                                 examples=["42,56", "100", 567.87])
    disc_memory: str = Field(...,
                             max_length=50,
                             description="Festplatte als String, höchstens 50 Zeichen.")
    screen_size: Decimal = Field(..., ge=0, max_digits=6, decimal_places=3,
                                 description="Bildschirmdiagonale als Zahl(wichtig)!",
                                 examples=["42,56", "100", 567.87])
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

class ChairOut(BaseProductOut):
    product_type: Literal["chair"] = "chair"

    height_min: int = Field(..., )
    height_max: int = Field(..., )
    max_weight: PositiveInt = Field(..., )
    description: str = Field(...,
                             max_length=200,
                             description="Sonstige Vorteile des Stuhls, höchstens 200 Zeichen.")


class KeyboardOut(BaseProductOut):
    product_type: Literal["keyboard"] = "keyboard"

    connection_style: str = Field(..., )
    layout: str = Field(..., )
    weight: PositiveInt = Field(..., )
    dimensions: str = Field(..., )
    description: str = Field(...,
                             max_length=200,
                             description="Sonstige Vorteile der Tastatur, höchstens 200 Zeichen.")


class MouseOut(BaseProductOut):
    product_type: Literal["mouse"] = "mouse"

    dpi: int = Field(..., )
    connection_style: str = Field(...,
                                  max_length=50)
    weight: int = Field(..., )
    battery: str = Field(...,
                         max_length=50)
    description: str = Field(...,
                             max_length=200)


class DockingStationOut(BaseProductOut):
    product_type: Literal["docking_station"] = "docking_station"

    display_port: int = Field(..., )
    hdmi: int = Field(..., )
    usb: str = Field(...,
                     max_length=80)
    usb_c: int = Field(..., )
    thunderbolt: int = Field(..., )
    ethernet: int = Field(..., )
    audio: int = Field(..., )


class WebcamOut(BaseProductOut):
    product_type: Literal["webcam"] = "webcam"

    fps: int = Field(..., )
    resolution: str = Field(...,
                            max_length=30)
    dfov_adjustable: bool = Field(..., )
    connection_style: str = Field(...,
                                  max_length=50)
    description: str = Field(...,
                             max_length=200)


class CableOut(BaseProductOut):
    product_type: Literal["cable"] = "cable"

    hdmi: str = Field(...,
                      max_length=80)
    ethernet: str = Field(...,
                          max_length=80)
    usb_c: str = Field(...,
                       max_length=80)
    display_port: str = Field(...,
                              max_length=80)


ProductOut = Annotated[Union[
    LaptopOut, MonitorOut, DeskOut, WorkstationOut, ChairOut, KeyboardOut, MouseOut, DockingStationOut, WebcamOut, CableOut],
             Field(discriminator="product_type")]


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

    model_config = ConfigDict(extra="forbid",from_attributes=True)


class PackageOut(BaseModel):
    id: UUID = Field(...,
                     description="Datenbank Paket-ID.")

    department_id: UUID = Field(...,
                                description="Datenbank Department-ID.")

    tier: Tier = Field(...,
                       description="'basic', 'premium' oder 'ultra'")

    items: List[PackageItemOut] = Field(default_factory=list,
                                        description="Inhalt des Paketes nach PackageItemIn-Schema.")

    model_config = ConfigDict(extra="forbid",from_attributes=True)


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

    model_config = ConfigDict(extra="forbid",from_attributes=True)
