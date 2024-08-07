from fastapi import APIRouter

from .auth.controllers.auth_controllers import auth_router
from .admin import router as admin_router
from .api import router as api_router


def get_apps_router() -> APIRouter:
    router = APIRouter()
    # Auth router
    router.include_router(auth_router)
    # Admin router
    router.include_router(admin_router)
    # API router
    router.include_router(api_router)

    return router
