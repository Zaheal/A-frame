import uuid

from fastapi import APIRouter

from src.schemas.auth_schemas import UserRead, UserCreate, UserUpdate
from src.models.core_models import User
from src.auth.user import get_user_manager, auth_backend
from src.auth.my_fastapi_users import MyFastAPIUsers

fastapi_users = MyFastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


def get_auth_router() -> APIRouter:
    router = APIRouter()
    router.include_router(
        fastapi_users.get_auth_router(backend=auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    router.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    router.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    router.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    router.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["user"],
    )
    return router


auth_router = get_auth_router()
