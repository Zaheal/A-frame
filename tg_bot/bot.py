from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.config.bot_config import get_config_bot
from src.config.redis_config import get_redis_settings

settings = get_config_bot()
storage_settings = get_redis_settings()

storage = RedisStorage.from_url(storage_settings.redis_url)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=storage)


async def start_bot():
    try:
        # await bot.send_message(settings.ADMIN_ID, f'Я запущен🥳.')
        pass
    except:
        pass


async def stop_bot():
    try:
        # await bot.send_message(settings.ADMIN_ID, 'Бот остановлен. За что?😔')
        pass
    except:
        pass
