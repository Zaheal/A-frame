from typing import Type, Generic

from fastapi import APIRouter

from fastapi_users import FastAPIUsers, schemas, models

from .register_func import get_register_router


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
