import asyncio
import contextlib

from src.auth.user import get_user_manager
from src.auth.user import UserManager
from src.database.db import db_helper
from src.models.core_models import User, get_user_db
from src.schemas.auth_schemas import UserCreate
from src.config.auth_config import get_auth_settings


get_users_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

settings = get_auth_settings()

default_email = settings.DEFAULT_EMAIL
default_tg_id = settings.DEFAULT_TG_ID
default_password = settings.DEFAULT_PWD
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(user_create=user_create, safe=False)
    return user


async def create_superuser(
    email: str = default_email,
    tg_id: int = default_tg_id,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        email=email,
        tg_id=tg_id,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )


if __name__ == "__main__":
    asyncio.run(create_superuser())
