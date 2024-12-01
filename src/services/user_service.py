from src.schemas.auth_schemas import UserUpdate, UserCreate
from src.utils.unitofwork import IUnitOfWork


class UserService:
    async def add_user(self, uow: IUnitOfWork, user: UserCreate):
        """

        :param uow:
        :param user:
        :return:
        """
        async with uow:
            user_id = await uow.users.create(user)
            return user_id

    async def get_users(self, uow: IUnitOfWork):
        """

        :param uow:
        :return model:
        """
        async with uow:
            users = await uow.users.get_multi()
            return users

    async def edit_user(self, uow: IUnitOfWork, user: dict, user_id: str):
        """

        :param uow:
        :param user_id:
        :param user:
        :return user_id:
        """
        async with uow:
            user_id = await uow.users.update(pk=user_id, data=user)
            return user_id

    async def remove_user(self, uow: IUnitOfWork, user_id: str):
        """

        :param uow:
        :param user_id:
        :return:
        """
        async with uow:
            await uow.users.delete(id=user_id)
            return

    async def get_user(self, uow: IUnitOfWork, **kwargs):
        """

        :param uow:
        :param **kwawrgs:
        :return user:
        """
        async with uow:
            user = await uow.users.get_single(**kwargs)
            return user
