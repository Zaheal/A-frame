import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base_model import Base

# Create a test database engine
engine = create_engine('sqlite:///test.db', echo=True)

# Create a session maker
Session = sessionmaker(bind=engine, class_=AsyncSession)


# Create a test database
async def create_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Drop the test database
async def drop_test_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db():
    await create_test_database()
    yield
    await drop_test_database()


@pytest.fixture
async def session(db):
    async with Session() as session:
        yield session
