from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship

from .base_model import Base
from ..database.db import db_helper

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)


class OAuthAccount(Base, SQLAlchemyBaseOAuthAccountTableUUID):
    pass


class User(Base, SQLAlchemyBaseUserTableUUID):
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


async def get_user_db(session: AsyncSession = Depends(db_helper.get_db_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
