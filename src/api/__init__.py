from fastapi import APIRouter

from .controllers.house_contollers import router as api_router

router = APIRouter(prefix="/home")
router.include_router(api_router)
