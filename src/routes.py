from fastapi import APIRouter

from .auth.controllers.auth_controllers import auth_router
from .admin.controllers import house_controllers, busy_time_controllers, user_controllers
from .api import router as api_router


def get_apps_router() -> APIRouter:
    router = APIRouter()
    # Auth router
    router.include_router(auth_router)
    # Admin router
    router.include_router(house_controllers.router)
    router.include_router(busy_time_controllers.router)
    router.include_router(user_controllers.router)
    # API router
    router.include_router(api_router)

    return router
