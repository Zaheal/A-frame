from .admin_router import admin_router
from .register_router import register_router
from .user_router import user_router

from aiogram import Router

router = Router()

router.include_router(admin_router)
router.include_router(register_router)
router.include_router(user_router)
