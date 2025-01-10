from datetime import date
import uuid

from pydantic import BaseModel

from .auth_schemas import User


class SHouse(BaseModel):
    id: int
    style: str
    color: str
    size: int
    cost: int
    add: str
    description: str

    busy_times: list["SReservation"]
    
    class Config:
        from_attributes = True


class SHouseAdd(BaseModel):
    style: str
    color: str
    size: int
    cost: int
    add: str
    description: str


class SHouseEdit(SHouseAdd):
    pass


class SHouseRead(SHouseAdd):
    pass


class SReservation(BaseModel):
    id: int
    start: date
    end: date
    full_price: int
    was_paid: bool = False
    add: bool

    house_id: int
    user_id: uuid.UUID

    house: "SHouse"
    user: "User"


class SReservationAdd(BaseModel):
    start: date
    end: date
    full_price: int
    was_paid: bool = False
    add: bool

    house_id: int

    class Config:
        from_attributes = True


class SReservationEdit(BaseModel):
    was_paid: bool = False


class SReservationRead(SReservationAdd):
    pass
