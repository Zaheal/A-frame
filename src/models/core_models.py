from typing import List
from datetime import date
from uuid import UUID

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTableUUID,
)

from sqlalchemy import ForeignKey, String, Integer, func, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date

from .base_model import Base
from src.database.db import db_helper


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    created_at: Mapped[date] = mapped_column(Date(), server_default=func.current_date())
    tg_id: Mapped[int] = mapped_column(Integer, nullable=True)
    number: Mapped[str] = mapped_column(String(length=18), nullable=True)
    name: Mapped[str] = mapped_column(String(length=100))
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )

    busy_times: Mapped[List["ReservationModel"]] = relationship(back_populates='user',
                                                                lazy='selectin')
    

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "tg_id": self.tg_id,
            "number": self.number,
            "name": self.name
        }
    
    
    def get_hashed_pwd(self):
        return self.hashed_password

    @property
    def is_authenticated(self):
        """
        Всегда возвращает True. Это способ узнать, был ли пользователь
        аутентифицирован в шаблонах.
        """
        return True


async def get_user_db(session: AsyncSession = Depends(db_helper.get_db_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


class HouseModel(Base):
    __tablename__ = 'houses'

    style: Mapped[str]
    color: Mapped[str]
    size: Mapped[int]
    cost: Mapped[int]
    add: Mapped[str]
    description: Mapped[str]

    busy_times: Mapped[List["ReservationModel"]] = relationship(back_populates='house',
                                                                lazy='selectin')
    temporary_busy_times: Mapped[List["TemporaryReservationModel"]] = relationship(back_populates='house',
                                                                                   lazy='selectin')
    
    def to_dict(self):
        return {
            "id": self.id,
            "style": self.style,
            "color": self.color,
            "size": self.size,
            "cost": self.cost,
            "add": self.add,
            "description": self.description,
        }


class ReservationModel(Base):
    __tablename__ = 'reservations'

    start: Mapped[date] = mapped_column(Date())
    end: Mapped[date] = mapped_column(Date())
    full_price: Mapped[int]
    was_paid: Mapped[bool] = mapped_column(Boolean(), default=False)
    add: Mapped[bool] = mapped_column(Boolean())

    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=True)

    house: Mapped["HouseModel"] = relationship(back_populates='busy_times',
                                               lazy='selectin')
    user: Mapped["User"] = relationship(back_populates='busy_times',
                                        lazy='selectin')
    
    def to_dict(self):
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "full_price": self.full_price,
            "was_paid": self.was_paid,
            "add": self.add,
            "house_id": self.house_id,
            "user_id": self.user_id,
        }


class TemporaryReservationModel(Base):
    __tablename__ = 'temporary_reservations'

    start: Mapped[date] = mapped_column(Date())
    end: Mapped[date] = mapped_column(Date())
    full_price: Mapped[int]
    was_paid: Mapped[bool] = mapped_column(Boolean(), default=False)
    add: Mapped[bool] = mapped_column(Boolean())
    name: Mapped[str] = mapped_column(String(length=100))
    email: Mapped[str] = mapped_column(String(length=50))
    number: Mapped[str] = mapped_column(String(length=18))

    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id"))

    house: Mapped["HouseModel"] = relationship(back_populates='temporary_busy_times',
                                               lazy='selectin')

    def to_dict(self):
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "full_price": self.full_price,
            "was_paid": self.was_paid,
            "add": self.add,
            "name": self.name,
            "email": self.email,
            "number": self.number,
            "house_id": self.house_id,
        }