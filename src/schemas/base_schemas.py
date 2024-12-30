from datetime import date
import uuid

from pydantic import BaseModel

from .auth_schemas import User
from ..models.core_models import VarOfPaid


class SHouse(BaseModel):
    id: int
    style: str
    color: str
    size: int
    cost: int
    location: str
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
    location: str
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
    was_paid: VarOfPaid = VarOfPaid.not_paid

    house_id: int
    user_id: uuid.UUID

    house: "SHouse"
    user: "User"


class SReservationAdd(BaseModel):
    start: date
    end: date
    full_price: int
    was_paid: VarOfPaid = VarOfPaid.not_paid

    house_id: int


class SReservationEdit(SReservationAdd):
    pass


class SReservationRead(SReservationAdd):
    pass
