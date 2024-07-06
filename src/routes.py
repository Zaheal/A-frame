from fastapi import APIRouter

from .controllers.auth_controllers import auth_router


def get_apps_router() -> APIRouter:
    router = APIRouter()
    router.include_router(auth_router)

    return router
