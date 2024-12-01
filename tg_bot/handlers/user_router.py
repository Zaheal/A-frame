from aiogram import Router, F
from aiogram.types import Message

from src.language.ru_lang import Dictionary
from src.config.bot_config import get_config_bot
from src.logger import get_logger

from tg_bot.keyboards.kbs import app_keyboard
from tg_bot.utils.utils import greet_user, get_about_us_text

user_router = Router()

logger = get_logger(__name__)
settings = get_config_bot()


@user_router.message(F.text == '🔙 Назад')
async def cmd_back_home(message: Message) -> None:
    """
    Обрабатывает нажатие кнопки "Назад".
    """
    await greet_user(message, is_new_user=False)


@user_router.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    kb = app_keyboard(user_id=message.from_user.id, first_name=message.from_user.first_name)
    await message.answer(get_about_us_text(), reply_markup=kb)