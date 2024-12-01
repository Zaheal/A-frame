import httpx
import re

from aiogram.types import Message

from tg_bot.keyboards.kbs import start_keyboard
from src.language.ru_lang import Dictionary
from src.logger import get_logger
from src.config.bot_config import get_config_bot

settings = get_config_bot()
logger = get_logger(__name__)


def get_about_us_text() -> str:
    return Dictionary["about_us_bot"]


async def greet_user(message: Message, is_new_user: bool) -> None:
    if is_new_user:
        await message.answer(
            f"{message.from_user.full_name}! {Dictionary["new_user_bot"]}",
            reply_markup=start_keyboard()
        )
    else:
        await message.answer(f"{message.from_user.full_name}! {Dictionary["old_user_bot"]}")


def format_bool(string: str):
    def replace_true_false(match):
        return match.group(0).capitalize()
    
    formatted_string = re.sub(r"\b(true|false)\b", replace_true_false, string)

    return formatted_string


class UserActions:
    async def get_user_by_tg(self, tg_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.BASE_SITE}/admin/get/user/tg/{tg_id}")
            user = response.text
        return user, response.status_code


    async def get_user_by_email(self, email: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.BASE_SITE}/admin/get/user/email/{email}")
            user = response.text
        return user, response.status_code


    async def update_user(self, user_data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{settings.BASE_SITE}/admin/update/user/{user_data["id"]}", json={"tg_id": user_data["tg_id"]})
            user = response.text
        return user, response.status_code


    async def create_user(self, user_data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.BASE_SITE}/admin/user/add", json=user_data)
            user = response.text
        return user, response.status_code


    async def confirm_email(self, email: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.BASE_SITE}/auth/request-verify-token", json=email)
        return response.status_code