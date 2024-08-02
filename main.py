import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.project_config import get_settings
from src.routes import get_apps_router
from src.tg_bot.bot import lifespan


def get_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        # lifespan=lifespan
    )
    application.include_router(get_apps_router())

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS.split(" "),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
