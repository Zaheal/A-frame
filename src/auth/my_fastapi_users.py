from typing import Type, Generic

from fastapi import APIRouter

from fastapi_users import FastAPIUsers, schemas, models

from .register_func import get_register_router
from .verify_func import get_verify_router
from .reset_pwd_func import get_reset_password_router


class MyFastAPIUsers(FastAPIUsers, Generic[models.UP, models.ID]):

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
    
    def get_verify_router(self, user_schema: Type[schemas.U]) -> APIRouter:
        """
        Return a router with e-mail verification routes.

        :param user_schema: Pydantic schema of a public user.
        """
        return get_verify_router(self.get_user_manager, user_schema)        

    def get_reset_password_router(self) -> APIRouter:
        """Return a reset password process router."""
        return get_reset_password_router(self.get_user_manager)
