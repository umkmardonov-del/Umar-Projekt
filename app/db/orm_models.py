# --- ORM-Models für SQLAlchemy bzw. Alembic ---
# --- path: /app/db/orm_models.py ---

from __future__ import annotations

from sqlalchemy import String, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Laptop(Base):
    __tablename__ = "laptops"

    laptop_id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    laptop_name: Mapped[str] = mapped_column(String(200),
                                             nullable=False)
    laptop_price: Mapped[int] = mapped_column(Integer,
                                       nullable=False)
