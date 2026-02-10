# --- Pydantic-Models für User ---
# --- path: /app/pydantic_models/auth/auth_orm.py ---

from pydantic import Field, EmailStr, SecretStr, BaseModel, StringConstraints, ConfigDict
from typing import Annotated
from uuid import UUID

PasswordString = Annotated[
    SecretStr, StringConstraints(min_length=8, max_length=24)]  #TODO Strip whitespace Field Validator
EmailString = Annotated[EmailStr, StringConstraints(max_length=256, strip_whitespace=True)]
NameString = Annotated[str, StringConstraints(min_length=2, max_length=100, strip_whitespace=True)]


# --- Eingabeschemata ---

class RegisterIn(BaseModel):
    email: EmailString = Field(...,
                               description="E-Mail Adresse.",
                               examples=["example@example.com"])

    password: PasswordString = Field(...,
                                     description="Passwort mit mindestens 8 und höchstens 24 Zeichen.",
                                     examples=["password", "59iubF!8"])

    name: NameString = Field(...,
                             description="Vorname, max, 100 Zeichen.")

    surname: NameString = Field(...,
                                description="Nachname, max. 100 Zeichen.")

    model_config = ConfigDict(extra="forbid")


class LoginIn(BaseModel):
    email: EmailStr = Field(...,
                            description="E-Mail Adresse.",
                            examples=["example@example.com"])

    password: PasswordString = Field(...,
                                     description="Passwort mit mindestens 8 und höchstens 24 Zeichen.",
                                     examples=["password", "59iubF!8"])

    model_config = ConfigDict(extra="forbid")


class RoleIn(BaseModel):
    name: str = Field(...,
                      max_length=20,
                      description="Name der Rolle.",
                      examples=["Admin", "Maintainer"])

    description: str = Field(max_length=256,
                             description="Rollenbeschreibung.")

    model_config = ConfigDict(extra="forbid")


class PermissionIn(BaseModel):
    code: str = Field(...,
                      max_length=100,
                      description="Permission Code.",
                      examples=["user:read", "admin:read"])

    description: str = Field(max_length=256,
                             description="Berechtigungsbeschreibung.")

    model_config = ConfigDict(extra="forbid")


class UserRoleIn(BaseModel):
    user_name: str = Field(...,)

    user_surname: str = Field(...,)

    role_names: list[str] = Field(...,)

    model_config = ConfigDict(extra="forbid")


class RolePermissionIn(BaseModel):
    role_name: str = Field(...,)

    permission_codes: list[str] = Field(...,)

    model_config = ConfigDict(extra="forbid")


# --- Ausgabeschemata ---

class UserOut(BaseModel):
    id: UUID = Field(...,
                     description="Automatisch generierte User ID.")

    email: EmailString = Field(...,
                               description="E-Mail Adresse.",
                               examples=["example@example.com"])

    name: NameString = Field(...,
                             description="Vorname, max, 100 Zeichen.")

    surname: NameString = Field(...,
                                description="Nachname, max. 100 Zeichen.")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class RoleOut(BaseModel):
    pass


class PermissionOut(BaseModel):
    pass


class Me(BaseModel):
    pass
