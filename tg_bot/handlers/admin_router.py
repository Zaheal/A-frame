from aiogram import Router, F
from aiogram.types import Message

from src.config.bot_config import get_config_bot

admin_router = Router()

settings = get_config_bot()


@admin_router.message(F.from_user.id.in_(map(lambda x: int(x), settings.ADMIN_ID.split(","))), F.text == "Админ панель")
async def admin_panel(message: Message):
    await message.answer(
        """
        Добро пожаловать в панель администратора. Здесь вы можете:\n"
         • Просматривать все текущие заявки\n"
         • Управлять статусами заявок\n"
         • Анализировать статистику\n\n"
        Для доступа к полному функционалу, пожалуйста, перейдите по ссылке ниже.\n"
        Мы постоянно работаем над улучшением и расширением возможностей панели.",
        """
    )