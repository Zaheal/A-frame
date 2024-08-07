from fastapi import APIRouter

from .controllers.house_controllers import router as house_router
from .controllers.user_controllers import router as user_router
from .controllers.reservation_controllers import router as reservation_router

router = APIRouter(prefix="/admin")

router.include_router(house_router)
router.include_router(user_router)
router.include_router(reservation_router)
