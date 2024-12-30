import uuid
from datetime import date

from fastapi_users import schemas


class User(schemas.BaseModel):
    tg_id: int | None = None
    number: str | None = None
    name: str
    created_at: date = date.today()



class UserRead(schemas.BaseUser[uuid.UUID]):
    tg_id: int | None = None
    number: str | None = None
    name: str
    created_at: date = date.today()


class UserCreate(schemas.BaseUserCreate):
    tg_id: int | None = None
    number: str | None = None
    name: str
    created_at: date = date.today()


class UserUpdate(schemas.BaseUserUpdate):
    tg_id: int | None = None
    number: str | None = None
    name: str
    created_at: date = date.today()
