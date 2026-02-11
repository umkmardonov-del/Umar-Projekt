# --- Funktionen/Klassen für User Permissions ---
# --- path: /app/security/permissions.py ---

from fastapi import Depends

from app.core.deps import auth_session_dep
from app.core.exceptions import NotPermittedError
from app.security.session_data import SessionData


class PermissionHandler:
    def __init__(self, scopes: list[str], permissions: list[str]) -> None:

        if not permissions or not scopes:
            raise AssertionError("Scopes/Permissions dürfen nicht leer sein.")

        self.scopes = scopes
        self.permissions = permissions
        self.required = [self.required_for(scope) for scope in scopes]

    async def __call__(self, data: SessionData = Depends(auth_session_dep)) -> set[str]:

        user_permissions = set(data["permissions"])

        permitted = any(required <= user_permissions for required in self.required)
        if not permitted:
            raise NotPermittedError()

        # TODO: Eventuell "X-Permissions-Needed" Header

        return user_permissions

    def required_for(self, scope: str) -> frozenset[str]:

        return frozenset(f"{scope}:{permission}" for permission in self.permissions)
