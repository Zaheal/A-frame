import re
from datetime import date
import uuid

from pydantic import BaseModel, EmailStr

from .auth_schemas import User
from ..models.core_models import VarOfPaid


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

    busy_times: list["SReservation"]


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


class SReservation(BaseModel):
    id: int
    email: EmailStr
    tg_id: int
    start: date
    end: date
    full_price: int
    was_paid: VarOfPaid = VarOfPaid.not_paid

    house_id: int
    # user_uuid: uuid.UUID
    user_id: uuid.UUID

    house: "SHouse"
    user: "User"


class SReservationAdd(BaseModel):
    email: EmailStr
    tg_id: int | None
    start: date
    end: date
    full_price: int
    was_paid: VarOfPaid = VarOfPaid.not_paid

    house_id: int
    user_id: uuid.UUID


class SReservationEdit(SReservationAdd):
    pass


class SReservationRead(SReservationAdd):
    pass
