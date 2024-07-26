from datetime import datetime
from typing import NewType

from pydantic import BaseModel


class SHouse(BaseModel):
    id: int
    style: str
    color: str
    air_conditioner: bool
    place: int
    size: int
    cost: int
    location: str
    bath: bool

    busy_times: list["SBusyTimeModel"]


class SHouseAdd(BaseModel):
    style: str
    color: str
    air_conditioner: bool
    place: int
    size: int
    cost: int
    location: str
    bath: bool


class SHouseEdit(SHouseAdd):
    pass


class SHouseRead(SHouseAdd):
    pass


class SBusyTimeModel(BaseModel):
    id: int
    start: datetime
    end: datetime
    full_price: int
    house_id: int
    house: "SHouse"


class SBusyTimeAdd(BaseModel):
    start: datetime
    end: datetime
    full_price: int
    house_id: int


class SBusyTimeEdit(SBusyTimeAdd):
    pass
