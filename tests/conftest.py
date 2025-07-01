import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from alembic import command
from alembic.config import Config

from ..main import app
from src.utils.unitofwork import UnitOfWork

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5433/test_db"


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def apply_migrations():
    config = Config('alembic.ini')
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    
    command.upgrade(config, "head")
    
    yield
    
    command.downgrade(config, "base")
    await _drop_test_db()


async def _drop_test_db():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute("DROP SCHEMA public CASCADE")
        await conn.execute("CREATE SCHEMA public")
    await engine.dispose()


@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        async with session.begin():
            yield session
            await session.rollback()
    await engine.dispose()


@pytest.fixture
def uow(db_session):
    class TestUOW(UnitOfWork):
        def __init__(self):
            self._session_factory = lambda: db_session
    return TestUOW()


@pytest.fixture
async def client(uow):
    app.dependency_overrides[UnitOfWork] = lambda: uow
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
