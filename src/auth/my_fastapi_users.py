from typing import Type, Generic, Optional

from fastapi import APIRouter

from fastapi_users import FastAPIUsers, schemas, models

from .func.verify_func import get_verify_router
from .func.reset_pwd_func import get_reset_password_router
from .func.oauth_func import get_oauth_router
from .func.register_func import get_register_router

from fastapi import APIRouter

from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.jwt import SecretType

try:
    from httpx_oauth.oauth2 import BaseOAuth2

except ModuleNotFoundError:  # pragma: no cover
    BaseOAuth2 = Type  # type: ignore


class MyFastAPIUsers(FastAPIUsers, Generic[models.UP, models.ID]):
    
    def get_verify_router(self, user_schema: Type[schemas.U]) -> APIRouter:
        """
        Return a router with e-mail verification routes.

        :param user_schema: Pydantic schema of a public user.
        """
        return get_verify_router(self.get_user_manager, user_schema)        

    def get_reset_password_router(self) -> APIRouter:
        """Return a reset password process router."""
        return get_reset_password_router(self.get_user_manager)
    

    def get_oauth_router(
        self,
        oauth_client: BaseOAuth2,
        backend: AuthenticationBackend,
        state_secret: SecretType,
        redirect_url: Optional[str] = None,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
    ) -> APIRouter:
        """
        Return an OAuth router for a given OAuth client and authentication backend.

        :param oauth_client: The HTTPX OAuth client instance.
        :param backend: The authentication backend instance.
        :param state_secret: Secret used to encode the state JWT.
        :param redirect_url: Optional arbitrary redirect URL for the OAuth2 flow.
        If not given, the URL to the callback endpoint will be generated.
        :param associate_by_email: If True, any existing user with the same
        e-mail address will be associated to this user. Defaults to False.
        :param is_verified_by_default: If True, the `is_verified` flag will be
        set to `True` on newly created user. Make sure the OAuth Provider you're
        using does verify the email address before enabling this flag.
        """
        return get_oauth_router(
            oauth_client,
            backend,
            self.get_user_manager,
            state_secret,
            redirect_url,
            associate_by_email,
            is_verified_by_default,
        )
    

    def get_register_router(
        self, user_schema: Type[schemas.U], user_create_schema: Type[schemas.UC]
    ) -> APIRouter:
        """
        Return a router with a register route.

        :param user_schema: Pydantic schema of a public user.
        :param user_create_schema: Pydantic schema for creating a user.
        """
        return get_register_router(
            self.get_user_manager, user_schema, user_create_schema
        )


