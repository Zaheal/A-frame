from fastapi import APIRouter

from .auth.controllers.auth_controllers import auth_router
from .admin.controllers import house_controllers, busy_time_controllers, user_controllers


def get_apps_router() -> APIRouter:
    router = APIRouter()
    router.include_router(auth_router)
    router.include_router(house_controllers.router)
    router.include_router(busy_time_controllers.router)
    router.include_router(user_controllers.router)

    return router
