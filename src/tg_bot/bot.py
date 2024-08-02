from contextlib import asynccontextmanager
from fastapi import FastAPI

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from ..config.tg_bot_config import get_bot_settings

settings = get_bot_settings()

bot = Bot(token=settings.TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """

    :type app: object
    """
    await bot.set_webhook(url=f"{settings.API_URL}/bot/webhook",
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    yield
    await bot.delete_webhook()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer('Привет!')
