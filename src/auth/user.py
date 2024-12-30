import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase

from src.models.core_models import User, get_user_db
from src.config.auth.strategy import get_jwt_strategy
from src.config.auth.transport import cookie_transport
from src.config.auth_config import get_auth_settings
from src.utils.worker import send_email_task
from src.config.redis_config import get_redis_settings
from src.language.ru_lang import Dictionary
from src.utils.pwd_validate import validate_password
from src.logger import get_logger

redis_settings = get_redis_settings()
settings = get_auth_settings()
logger = get_logger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def on_after_request_verify(self, user, token, request = None):
        activation_url = request.url_for("verify:verify", token=token)
        result = send_email_task.delay(email_to=user.email, body=Dictionary["confirm_email"] + f" {activation_url}")
        logger.info(f"{result.get()}")


    async def on_after_forgot_password(self, user, token, request = None):
        actiovation_url = request.url_for("reset:edit_password", token=token)
        result = send_email_task.delay(email_to=user.email, body=Dictionary["reset_pwd"] + f" {actiovation_url}")
        logger.info(f"{result.get()}")

    async def validate_password(
        self,
        password: str,
        email: str,
    ) -> None:
        await validate_password(password, email)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True, optional=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True, optional=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
