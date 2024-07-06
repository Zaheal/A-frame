from typing import List
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from .base_model import Base


class HouseModel(Base):
    __tablename__ = 'houses'

    name: Mapped[str]
    color: Mapped[str]
    air_conditioner: Mapped[bool]
    place: Mapped[int]
    size: Mapped[int]
    cost: Mapped[int]
    space: Mapped[int]

    bath_id: Mapped[int] = mapped_column(ForeignKey("bathes.id", ondelete='CASCADE'))
    bath: Mapped["BathModel"] = relationship(back_populates='houses')
    prices: Mapped[List["PriceHouseModel"]] = relationship(back_populates='house', cascade='all, delete')


class BathModel(Base):
    __tablename__ = 'bathes'

    name: Mapped[str]
    liter: Mapped[int]
    space: Mapped[int]
    cost: Mapped[int]

    houses: Mapped[List["HouseModel"]] = relationship(back_populates='bath', cascade='all, delete')
    prices: Mapped[List["PriceBathModel"]] = relationship(back_populates='bath', cascade='all, delete')


class PriceHouseModel(Base):
    __tablename__ = 'price_houses'

    name: Mapped[str]
    start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    full_price: Mapped[int]
    house_id: Mapped[int] = mapped_column(ForeignKey("houses.id", ondelete='CASCADE'))

    house: Mapped["HouseModel"] = relationship(back_populates='prices', cascade='all, delete')


class PriceBathModel(Base):
    __tablename__ = 'price_bathes'

    name: Mapped[str]
    start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    full_price: Mapped[int]
    bath_id: Mapped[int] = mapped_column(ForeignKey("bathes.id", ondelete='CASCADE'))

    bath: Mapped["BathModel"] = relationship(back_populates="prices", cascade="all, delete")
