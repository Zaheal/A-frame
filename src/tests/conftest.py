from os import environ
import asyncpg

import pytest
from httpx import AsyncClient, ASGITransport
from alembic.command import upgrade, downgrade
from alembic.config import Config

from main import app
from src.config.db_config import get_db_settings
from src.database.db import Database
from src.models.base_model import Base

environ["TESTING"] = "True"
settings = get_db_settings()

db_instance = Database(settings.database_url)


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=f"http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def session():
    async with db_instance.engine.begin() as connection:

        async with db_instance.session_factory(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()

# @pytest.fixture(scope="session")
# async def create_migrations():
#     db = Database(settings.database_url, settings.DB_ECHO_LOG)
#
#     config = Config("alembic.ini")
#     config.set_main_option("script_location", "migrations")
#     config.set_main_option("sqlalchemy.url", settings.database_url)
#     upgrade(config, "head")
#     yield
#     downgrade(config, "base")



