import uuid

from fastapi_users import schemas


class User(schemas.BaseModel):
    tg_id: int



class UserRead(schemas.BaseUser[uuid.UUID]):
    tg_id: int


class UserCreate(schemas.BaseUserCreate):
    id: uuid.UUID
    tg_id: int


class UserUpdate(schemas.BaseUserUpdate):
    pass
