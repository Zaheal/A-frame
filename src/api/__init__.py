from fastapi import APIRouter

from .controllers.house_controllers import router as house_router
from .controllers.user_reservation_controllers import router as busy_time_router

router = APIRouter(prefix="/home")

router.include_router(house_router)
router.include_router(busy_time_router)
