import re
from datetime import date
import uuid

from pydantic import BaseModel, field_validator

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

    busy_times: list["SBusyTime"]


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


class SBusyTime(BaseModel):
    id: int
    email: str
    number: str
    start: date
    end: date
    full_price: int
    house_id: int
    user_id: uuid.UUID
    was_paid: VarOfPaid = VarOfPaid.not_paid

    house: "SHouse"


class SBusyTimeAdd(BaseModel):
    email: str
    number: str
    start: date
    end: date
    full_price: int
    house_id: int
    was_paid: VarOfPaid = VarOfPaid.not_paid


    @field_validator("number")
    @classmethod
    def number_is_valid(cls, values: str) -> str:
        if not re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                        values):
            raise ValueError("Номер телефона должен начинаться с +7, 7 или 8 и содержать от 11 до 12 цифр")
        return values


class SBusyTimeEdit(SBusyTimeAdd):
    pass


class SBusyTimeRead(SBusyTimeAdd):
    pass
