from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.status import HTTP_400_BAD_REQUEST
from aiogram.types import Update
from redis import asyncio as aioredis
from prometheus_fastapi_instrumentator import Instrumentator

from src.config.project_config import get_settings
from src.config.bot_config import get_config_bot
from src.config.redis_config import get_redis_settings
from src.routes import get_apps_router
from src.logger import get_logger
from src.pages.template import templates
from src.middleware import LoggingMiddleware

from tg_bot.bot import bot, dp, start_bot, stop_bot
from tg_bot.handlers import router


logger = get_logger(__name__)
bot_settings = get_config_bot()
redis_settings = get_redis_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # logger.info("Application startup")
    # dp.include_router(router)
    # await start_bot()
    # webhook_url = bot_settings.get_webhook_url()
    # await bot.set_webhook(url=webhook_url,
    #                       allowed_updates=dp.resolve_used_update_types(),
    #                       drop_pending_updates=True
    #                       )
    # logger.info(f"Webhook set to {webhook_url}")
    redis = aioredis.from_url(redis_settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache") 
    yield
    # logger.info("Aplication shutdown")
    # await bot.delete_webhook()
    # await stop_bot()
    # logger.info("Webhook deleted")


def get_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
    )

    Instrumentator().instrument(application).expose(application)

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


    @application.exception_handler(HTTPException)
    async def http_errors(request: Request, exc: HTTPException):
        return templates.TemplateResponse(request, "/error-page.html", context={"status_code": exc.status_code, "detail": exc.detail})


    application.mount("/", StaticFiles(directory="frontend"), name='static')


    @application.get("/{full_path:path}")
    async def catch_all(full_path: str):
        raise HTTPException(status_code=404)


    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS.split(" "),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(LoggingMiddleware)
    application.add_middleware(GZipMiddleware, minimum_size=1000)

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000)
