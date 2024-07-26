from ..schemas.auth_schemas import UserUpdate, UserCreate
from ..utils.unitofwork import IUnitOfWork


class UserService:
    async def add_user(self, uow: IUnitOfWork, user: UserCreate):
        """

        :param uow:
        :param user:
        :return:
        """
        users_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.create(users_dict)
            return user_id

    async def get_users(self, uow: IUnitOfWork):
        """

        :param uow:
        :return model:
        """
        async with uow:
            users = await uow.users.get_multi()
            return users

    async def edit_user(self, uow: IUnitOfWork, user: UserUpdate, user_id: int):
        """

        :param uow:
        :param user_id:
        :param user:
        :return user_id:
        """
        users_dict = user.model_dump()
        async with uow:
            user_id = await uow.users.update(pk=user_id, data=users_dict)
            return user_id

    async def remove_user(self, uow: IUnitOfWork, user_id: int):
        """

        :param uow:
        :param user_id:
        :return:
        """
        async with uow:
            await uow.users.delete(pk=user_id)
            return
