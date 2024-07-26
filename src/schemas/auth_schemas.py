import uuid

from fastapi_users import schemas


class OAuthAccount(schemas.BaseOAuthAccount):
    pass


class User(schemas.BaseModel):
    pass


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
