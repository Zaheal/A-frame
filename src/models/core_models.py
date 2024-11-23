from typing import List
from datetime import date, timedelta
from uuid import UUID
import enum

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTableUUID,
)

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date

from .base_model import Base
from ..database.db import db_helper


class VarOfPaid(str, enum.Enum):
    paid = "paid"
    not_paid = "not_paid"


class User(SQLAlchemyBaseUserTableUUID, Base):
    tg_id: Mapped[int] = mapped_column(Integer, nullable=True)

    busy_times: Mapped[List["ReservationModel"]] = relationship(back_populates='user',
                                                                lazy='selectin')
    

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "tg_id": self.tg_id
        }

    @property
    def is_authenticated(self):
        """
        Всегда возвращает True. Это способ узнать, был ли пользователь
        аутентифицирован в шаблонах.
        """
        return True


async def get_user_db(session: AsyncSession = Depends(db_helper.get_db_session)):
    yield SQLAlchemyUserDatabase(session, User)


class HouseModel(Base):
    __tablename__ = 'houses'

    style: Mapped[str]
    color: Mapped[str]
    air_conditioner: Mapped[bool]
    place: Mapped[int]
    size: Mapped[int]
    cost: Mapped[int]
    location: Mapped[str]
    bath: Mapped[bool]

    busy_times: Mapped[List["ReservationModel"]] = relationship(back_populates='house',
                                                                lazy='selectin')


class ReservationModel(Base):
    __tablename__ = 'reservations'

    email: Mapped[str] = mapped_column(String(length=320))
    start: Mapped[date] = mapped_column(Date(), server_default=f"{date.today()}")
    end: Mapped[date] = mapped_column(Date(), server_default=f"{date.today() + timedelta(days=1)}")
    full_price: Mapped[int]
    was_paid: Mapped[str] = mapped_column(String(), default="not_paid")

    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=True)

    house: Mapped["HouseModel"] = relationship(back_populates='busy_times',
                                               lazy='selectin')
    user: Mapped["User"] = relationship(back_populates='busy_times',
                                        lazy='selectin')
