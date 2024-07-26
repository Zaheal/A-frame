from typing import List
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date

from .base_model import Base


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

    busy_times: Mapped[List["BusyTimeModel"]] = relationship(back_populates='house',
                                                             lazy='selectin')


class BusyTimeModel(Base):
    __tablename__ = 'busy_times'

    email: Mapped[str] = mapped_column(String(length=320), nullable=False)
    number: Mapped[str] = mapped_column(String(12), nullable=False)
    start: Mapped[date] = mapped_column(Date(), server_default=f"{date.today()}")
    end: Mapped[date] = mapped_column(Date(), server_default=f"{date.today()}")
    full_price: Mapped[int]
    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id"))

    house: Mapped["HouseModel"] = relationship(back_populates='busy_times',
                                               lazy='selectin')
