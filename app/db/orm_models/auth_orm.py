# --- ORM-Models für Auth (User/Rollen/Permissions) ---
# --- path: /app/db/orm_models/auth_orm.py ---

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.orm_models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),
                                     primary_key=True,
                                     default=uuid4)

    name: Mapped[str] = mapped_column(String(100),
                                      nullable=False)
    surname: Mapped[str] = mapped_column(String(100),
                                         nullable=False)

    email: Mapped[str] = mapped_column(String(255),
                                       nullable=False,
                                       unique=True,
                                       index=True)

    pw_hash: Mapped[str] = mapped_column(String(255),
                                         nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean(),
                                            nullable=False,
                                            server_default=text("true"),
                                            index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(), )

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now(), )

    user_roles: Mapped[List["UserRole"]] = relationship(back_populates="user",
                                                        cascade="all, delete-orphan",
                                                        passive_deletes=True, )

    roles = association_proxy("user_roles", "role")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)

    name: Mapped[str] = mapped_column(String(50),
                                      nullable=False,
                                      unique=True,
                                      index=True)

    description: Mapped[str | None] = mapped_column(String(255),
                                                    nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(), )

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now(), )

    user_roles: Mapped[List["UserRole"]] = relationship(back_populates="role",
                                                        cascade="all, delete-orphan",
                                                        passive_deletes=True, )

    users = association_proxy("user_roles", "user")

    role_permissions: Mapped[List["RolePermission"]] = relationship(back_populates="role",
                                                                    cascade="all, delete-orphan",
                                                                    passive_deletes=True, )

    permissions = association_proxy("role_permissions", "permission")


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)

    code: Mapped[str] = mapped_column(String(100),
                                      nullable=False,
                                      unique=True,
                                      index=True)

    description: Mapped[str | None] = mapped_column(String(255),
                                                    nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(), )

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now(), )

    role_permissions: Mapped[List["RolePermission"]] = relationship(back_populates="permission",
                                                                    cascade="all, delete-orphan",
                                                                    passive_deletes=True, )

    roles = association_proxy("role_permissions", "role")


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_roles_user_id_role_id"),)

    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),
                                          ForeignKey("users.id", ondelete="CASCADE"),
                                          primary_key=True, )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id",
                                                    ondelete="CASCADE"),
                                         primary_key=True, )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(), )

    user: Mapped["User"] = relationship(back_populates="user_roles")

    role: Mapped["Role"] = relationship(back_populates="user_roles")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (UniqueConstraint("role_id", "permission_id",
                                       name="uq_role_permissions_role_id_permission_id"),)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id",
                                                    ondelete="CASCADE"),
                                         primary_key=True,)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id",
                                                          ondelete="CASCADE"),
                                               primary_key=True,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),)

    role: Mapped["Role"] = relationship(back_populates="role_permissions")

    permission: Mapped["Permission"] = relationship(back_populates="role_permissions")
