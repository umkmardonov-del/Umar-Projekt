# --- ORM-Models für User & Rollen ---
# --- path: /app/db/orm_models/users.py ---

from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID

from app.db.orm_models.products import Base

class User(Base):
    __tablename__ = "users"

    id:

    name:

    surname:

    email:

    pw_hash:

    role: