# --- ORM-Models für SQLAlchemy bzw. Alembic ---
# --- path: /app/db/orm_models.py ---

from __future__ import annotations

from enum import Enum
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, CheckConstraint, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ENUM as PGENUM
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from uuid import UUID, uuid4


class Base(DeclarativeBase, AsyncAttrs):
    pass


# --- Basis-Tabelle für Produkte ---

class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),
                                              primary_key=True,
                                              default=uuid4)
    name: Mapped[str] = mapped_column(String(200),
                                      nullable=False)
    price: Mapped[float]  = mapped_column(Float,
                                          nullable=False,
                                          default=0)

    # Discriminator für Polymorphie (String → flexibel für neue Typen)
    product_type: Mapped[str] = mapped_column(String(50),
                                              nullable=False,
                                              index=True)

    # Beziehung zurück zu PackageItem (Association-Object)
    package_items: Mapped[List["PackageItem"]] = relationship(back_populates="product")

    __mapper_args__ = {
        "polymorphic_on": product_type,
        "polymorphic_identity": "product",  # Basistyp
    }

# --- Einzelne Produkte und deren Spezifikationen ---

class Monitor(Product):
    __tablename__ = "monitors"

    resolution: Mapped[int] = mapped_column(Integer,
                                            nullable=False)
    latency: Mapped[int] = mapped_column(Integer,
                                         nullable=False)
    refresh_rate: Mapped[int] = mapped_column(Integer,
                                              nullable=False)
    power_usage: Mapped[float] = mapped_column(Float,
                                               nullable=False)
    screen_size: Mapped[str] = mapped_column(String(20),
                                             nullable=False)
    connectors: Mapped[str] = mapped_column(String(200),
                                            nullable=False)

    __mapper_args__ = {"polymorphic_identity": "monitor"}


class Laptop(Product):
    __tablename__ = "laptops"

    processor: Mapped[str] = mapped_column(String(50),
                                           nullable=False)
    operating_system: Mapped[str] = mapped_column(String(50),
                                                  nullable=False)
    memory: Mapped[str] = mapped_column(String(50),
                                        nullable=False)
    disc_memory: Mapped[str] = mapped_column(String(50),
                                             nullable=False)
    screen_size: Mapped[int] = mapped_column(Integer,
                                             nullable=False)
    resolution: Mapped[str] = mapped_column(String(20),
                                            nullable=False)
    refresh_rate: Mapped[int] = mapped_column(Integer,
                                              nullable=False)
    graphics_card: Mapped[str] = mapped_column(String(50))
    camera: Mapped[str] = mapped_column(String(50),
                                        nullable=False)

    __mapper_args__ = {"polymorphic_identity": "laptop"}


class Desk(Product):
    height_adjustable: Mapped[bool] = mapped_column(Boolean,
                                            nullable=False)
    dimensions: Mapped[str] = mapped_column(String(20),
                                            nullable=False)
    description: Mapped[str] = mapped_column(String(200),
                                             nullable=False)


# --- Tabelle für die einzelnen Abteilungen ---

class Department(Base):
    __tablename__ = "departments"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),
                                      primary_key=True,
                                      default=uuid4)
    name: Mapped[str] = mapped_column(String(100),
                                      unique=True,
                                      nullable=False)

    packages: Mapped[List["Package"]] = relationship(
        back_populates="department", cascade="all, delete-orphan"
    )


# --- Tabellen, die mit den Paketen zu tun haben ---

class Tier(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ULTRA = "ultra"


class Package(Base):
    __tablename__ = "packages"
    __table_args__ = (
        UniqueConstraint("department_id", "tier", name="uq_packages_department_tier"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),
                                     primary_key=True,
                                     default=uuid4)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("department.id", ondelete="CASCADE"),
                                              nullable=False)
    tier: Mapped[Tier] = mapped_column(PGENUM(Tier, name="tier", create_type=True),
                                       nullable=False)

    department: Mapped["Department"] = relationship(back_populates="packages")

    # Association-Object: Items mit Zusatzfeldern (quantity)
    items: Mapped[List["PackageItem"]] = relationship(
        back_populates="package", cascade="all, delete-orphan"
    )

    # Optionaler Komfort: direkt auf die Produkte zugreifen (READ-ONLY)
    products = association_proxy("items", "product")


class PackageItem(Base):
    __tablename__ = "package_items"
    __table_args__ = (
        UniqueConstraint("package_id", "product_id", name="uq_package_items_unique"),
        CheckConstraint("quantity > 0", name="ck_package_items_quantity_positive"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),
                                     primary_key=True,
                                     default=uuid4)
    package_id: Mapped[UUID] = mapped_column(ForeignKey("packages.id",ondelete="CASCADE"),
                                             nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"),
                                             nullable=False)
    quantity: Mapped[int] = mapped_column(Integer,
                                          nullable=False,
                                          default=1)

    package: Mapped["Package"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="package_items")
