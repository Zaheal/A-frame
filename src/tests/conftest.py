from os import environ

import pytest
from fastapi_users.authentication import AuthenticationBackend
from httpx import AsyncClient, ASGITransport

from main import app
from src.database.db import db_helper
from src.models.base_model import Base
from src.models.core_models import get_user_db
from src.auth.user import get_user_manager, UserManager, auth_backend
from src.schemas.auth_schemas import UserCreate
from src.config.auth.strategy import get_jwt_strategy

environ["TESTING"] = "True"

json = UserCreate(
        email="zakharlepskie@gmail.com",
        tg_id="1836141330",
        password="adminpwd",
        is_active=True,
        is_superuser=True,
        is_verified=True,
)


@pytest.fixture(scope="function")
async def client():
    """
    Подключение к асинхронному клиенту

    :return:
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=f"http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def prepare_db():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def session(prepare_db):
    """
    Подключение к сессии

    :return:
    """
    session_factory = db_helper.session_factory
    session = session_factory()
    yield session
    await session.close()


@pytest.fixture(scope="function")
async def authorized_client(client):
    ...