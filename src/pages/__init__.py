from fastapi import APIRouter

from .home import router as home_router
from .auth import router as auth_router
from .profile import router as profile_router

router = APIRouter(tags=["pages"])

router.include_router(home_router)
router.include_router(auth_router)
router.include_router(profile_router)
