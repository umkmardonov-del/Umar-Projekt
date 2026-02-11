# --- Pydantic-Models für User ---
# --- path: /app/pydantic_models/auth/auth_orm.py ---

from datetime import datetime
from pydantic import Field, EmailStr, SecretStr, BaseModel, StringConstraints, ConfigDict
from typing import Annotated, Optional
from uuid import UUID

#TODO Strip whitespace Field Validator
PasswordString = Annotated[SecretStr, StringConstraints(min_length=8, max_length=24)]
EmailString = Annotated[EmailStr, StringConstraints(max_length=256, strip_whitespace=True, to_lower=True)]
NameString = Annotated[str, StringConstraints(min_length=2, max_length=100, strip_whitespace=True)]
CodeString = Annotated[str, StringConstraints(min_length=5, max_length=100, strip_whitespace=True, to_lower=True)]
DescriptionString = Annotated[str, StringConstraints(max_length=256, strip_whitespace=True)]


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
    name: NameString = Field(...,
                             description="Name der Rolle.",
                             examples=["Admin", "Maintainer"])

    description: DescriptionString = Field(description="Rollenbeschreibung.")

    model_config = ConfigDict(extra="forbid")


class PermissionIn(BaseModel):
    code: CodeString = Field(...,
                             description="Permission Code, max 100 Zeichen.",
                             examples=["user:read", "admin:read"])

    description: DescriptionString = Field(description="Berechtigungsbeschreibung.")

    model_config = ConfigDict(extra="forbid")


class UserRoleIn(BaseModel):
    email: EmailString = Field(...,
                               description="Email Adresse.")

    role_name: NameString = Field(...,
                                  description="Rollenname.")

    model_config = ConfigDict(extra="forbid")


class RolePermissionIn(BaseModel):
    role_name: NameString = Field(...,
                                  description="Rollenname.")

    permission_code: CodeString = Field(...,
                                        description="Permission Code, max 100 Zeichen.")

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

    created_at: datetime = Field(...,
                                 description="Erstellungsdatum des User-Accounts.")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class RoleOut(BaseModel):
    id: int = Field(...,
                    description="Automatisch generierte Role ID.")

    name: NameString = Field(...,
                      description="Rollenname.")

    description: Optional[str] = Field(max_length=256,
                                       description="Rollenbeschreibung.")

    created_at: datetime = Field(...,
                                 description="Erstellungsdatum der Rolle.")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class PermissionOut(BaseModel):
    id: int = Field(...,
                    description="Automatisch generierte Permission ID.")

    code: NameString = Field(...,
                      description="Permission code.")

    description: Optional[str] = Field(max_length=256,
                                       description="Berechtigungsbeschreibung.")

    created_at: datetime = Field(...,
                                 description="Erstellungsdatum der Berechtigung.")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class UserRoleOut(BaseModel):
    user_id: UUID = Field(...,
                          description="User ID.")

    role_id: int = Field(...,
                         description="Role ID.")

    created_at: datetime = Field(...,
                                 description="Datum der Rollenzuweisung an den User.")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class RolePermissionOut(BaseModel):
    role_id: int = Field(...,
                         description="Role ID.")

    permission_id: int = Field(...,
                               description="Permission ID.")

    created_at: datetime = Field(...,
                                 description="Datum der Berechtigungszuweisung an die Rolle.")

    model_config = ConfigDict(extra="forbid", from_attributes=True)


class Me(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)
