# from contextlib import asynccontextmanager
# from fastapi import FastAPI
import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config.tg_bot_config import get_bot_settings
from handlers import user_handlers

settings = get_bot_settings()
dp: Dispatcher = Dispatcher()


async def main():
    bot = Bot(token=settings.TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(user_handlers.router)
    # dp.include_router(register_handlers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    asyncio.run(main())
