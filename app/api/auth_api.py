# --- Endpunkte für User-Authentifizierung ---
# --- path: app/api/auth_api.py ---

from fastapi import Request, Response, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import postgres_dep, session_store_dep, auth_session_dep
from app.pydantic_models.auth_models import RegisterIn, UserOut, LoginIn
from app.security.session_store import SessionStore
from app.security.session_data import SessionData
from app.service.auth_service import register_user_service, create_auth_session_service, login_user_service, \
    logout_user_service

user_router = APIRouter(prefix="auth", tags=["auth", "user"])


@user_router.post("/register", response_model=UserOut)
async def register_user_endpoint(payload: RegisterIn,
                                 response: Response,
                                 session: AsyncSession = Depends(postgres_dep),
                                 store: SessionStore = Depends(session_store_dep)) -> UserOut:
    user = await register_user_service(session, payload=payload)

    user_dto = await create_auth_session_service(session, store, response=response, user=user)

    return user_dto


@user_router.post("/login", response_model=UserOut)
async def login_user_endpoint(payload: LoginIn,
                              response: Response,
                              session: AsyncSession = Depends(postgres_dep),
                              store: SessionStore = Depends(session_store_dep)) -> UserOut:
    user = await login_user_service(session, payload=payload)

    user_dto = await create_auth_session_service(session, store, response=response, user=user)

    return user_dto


@user_router.post("logout", status_code=204)
async def logout_user_endpoint(request: Request,
                               response: Response,
                               store: SessionStore = Depends(session_store_dep),
                               data: SessionData = Depends(auth_session_dep)) -> None:

    await logout_user_service(store, data, request=request, response=response)
