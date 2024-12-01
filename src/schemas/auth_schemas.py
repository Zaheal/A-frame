import uuid

from fastapi_users import schemas


class User(schemas.BaseModel):
    tg_id: int | None



class UserRead(schemas.BaseUser[uuid.UUID]):
    tg_id: int | None


class UserCreate(schemas.BaseUserCreate):
    tg_id: int | None


class UserUpdate(schemas.BaseUserUpdate):
    tg_id: int | None
