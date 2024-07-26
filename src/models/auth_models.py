from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .base_model import Base
from ..database.db import db_helper

from fastapi_users.db import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable,
)


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass


async def get_user_db(session: AsyncSession = Depends(db_helper.get_db_session)):
    yield SQLAlchemyUserDatabase(session, User)
