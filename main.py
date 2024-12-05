from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_400_BAD_REQUEST
from aiogram.types import Update

from src.config.project_config import get_settings
from src.config.bot_config import get_config_bot
from src.routes import get_apps_router
from src.logger import get_logger
from src.middlewares.cookies_middleware import CookiesMiddleware

from tg_bot.bot import bot, dp, start_bot, stop_bot
from tg_bot.handlers import router


logger = get_logger(__name__)
bot_settings = get_config_bot()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    dp.include_router(router)
    await start_bot()
    webhook_url = bot_settings.get_webhook_url()
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True
                          )
    logger.info(f"Webhook set to {webhook_url}")
    yield
    logger.info("Aplication shutdown")
    await bot.delete_webhook()
    await stop_bot()
    logger.info("Webhook deleted")


def get_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        lifespan=lifespan,
    )

    application.include_router(get_apps_router())
    

    @application.post("/webhook")
    async def webhook(request: Request) -> None:
        try:
            update = Update.model_validate(await request.json(), context={"bot": bot})
            await dp.feed_webhook_update(bot=bot, update=update)
            logger.info("Update processed")
        except Exception as e:
            logger.error("Webhook error", exc_info=e)
            return HTTPException(HTTP_400_BAD_REQUEST, e)
        

    application.mount("/", StaticFiles(directory="frontend"), name='static')

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS.split(" "),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(CookiesMiddleware)
    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000)
