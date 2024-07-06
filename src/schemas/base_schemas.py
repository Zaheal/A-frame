from datetime import datetime

from pydantic import BaseModel


class SHouse(BaseModel):
    name: str
    color: str
    air_conditioner: bool
    place: int
    size: int
    cost: int
    space: int
    bath_id: int
    bath: "SBath"
    prices: list["SPriceHouse"]


class SBath(BaseModel):
    name: str
    liter: int
    space: int
    cost: int
    prices: list["SPriceHouse"]
    houses: list["SHouse"]


class SPriceHouse(BaseModel):
    name: str
    start: datetime
    end: datetime
    full_price: int
    house_id: int
    house: "SHouse"


class SPriceBath(BaseModel):
    name: str
    start: datetime
    end: datetime
    full_price: int
    bath_id: int
    bath: "SBath"
