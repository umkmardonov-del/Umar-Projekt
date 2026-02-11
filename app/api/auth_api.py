# --- Endpunkte für User-Authentifizierung ---
# --- path: app/api/auth_api.py ---

from fastapi import Request, Response, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import postgres_dep, session_store_dep, auth_session_dep
from app.pydantic_models.auth_models import (RegisterIn, UserOut, LoginIn, RoleIn, RoleOut, PermissionIn, PermissionOut,
                                             UserRoleIn, UserRoleOut, RolePermissionIn, RolePermissionOut)
from app.security.permissions import PermissionHandler
from app.security.session_store import SessionStore
from app.security.session_data import SessionData
from app.service.auth_service import (register_user_service, create_auth_session_service, login_user_service,
                                      logout_user_service, create_role_service, create_permission_service,
                                      create_user_role_service, create_role_permission_service)

user_router = APIRouter(tags=["auth", "user"])
admin_router = APIRouter(prefix="/auth", tags=["auth", "admin"])


# ------- User Routen -------
@user_router.post("/register", status_code=201, response_model=UserOut)
async def register_user_endpoint(payload: RegisterIn,
                                 response: Response,
                                 session: AsyncSession = Depends(postgres_dep),
                                 store: SessionStore = Depends(session_store_dep)) -> UserOut:

    user = await register_user_service(session, payload=payload)

    user_dto = await create_auth_session_service(session, store, response=response, user_orm=user)

    return user_dto


@user_router.post("/login", response_model=UserOut)
async def login_user_endpoint(payload: LoginIn,
                              response: Response,
                              session: AsyncSession = Depends(postgres_dep),
                              store: SessionStore = Depends(session_store_dep)) -> UserOut:

    user = await login_user_service(session, payload=payload)

    user_dto = await create_auth_session_service(session, store, response=response, user_orm=user)

    return user_dto


@user_router.post("/logout", status_code=204, dependencies=[Depends(auth_session_dep)])
async def logout_user_endpoint(request: Request,
                               response: Response,
                               store: SessionStore = Depends(session_store_dep),
                               data: SessionData = Depends(auth_session_dep)) -> None:

    await logout_user_service(store, data, request=request, response=response)


# ------- Admin Routen -------
@admin_router.post("/create_role", status_code=201,
                   dependencies=[Depends(auth_session_dep), Depends(PermissionHandler(["admin"],["write"]))])
async def create_role_endpoint(payload: RoleIn,
                               session: AsyncSession = Depends(postgres_dep)) -> RoleOut:

    role_dto = await create_role_service(session, payload)

    return role_dto


@admin_router.post("/create_permission", status_code=201,
                   dependencies=[Depends(auth_session_dep), Depends(PermissionHandler(["admin"],["write"]))])
async def create_permission_endpoint(payload: PermissionIn,
                                     session: AsyncSession = Depends(postgres_dep)) -> PermissionOut:

    permission_dto = await create_permission_service(session, payload)

    return permission_dto


@admin_router.post("/create_ur", status_code=201,
                   dependencies=[Depends(auth_session_dep), Depends(PermissionHandler(["admin"],["write"]))])
async def create_user_role_endpoint(payload: UserRoleIn,
                                    session: AsyncSession = Depends(postgres_dep)) -> UserRoleOut:

    user_role_dto = await create_user_role_service(session, payload)

    return user_role_dto


@admin_router.post("/create_rp", status_code=201,
                   dependencies=[Depends(auth_session_dep), Depends(PermissionHandler(["admin"],["write"]))])
async def create_role_permission_endpoint(payload: RolePermissionIn,
                                          session: AsyncSession = Depends(postgres_dep)) -> RolePermissionOut:

    role_permission_dto = await create_role_permission_service(session, payload)

    return role_permission_dto
