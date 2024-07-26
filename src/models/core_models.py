from typing import List
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

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
                                                             cascade='all, delete',
                                                             lazy='selectin')


class BusyTimeModel(Base):
    __tablename__ = 'busy_times'

    start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    full_price: Mapped[int]
    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id", ondelete='CASCADE'))

    house: Mapped["HouseModel"] = relationship(back_populates='busy_times',
                                               cascade='all, delete',
                                               lazy='selectin')
