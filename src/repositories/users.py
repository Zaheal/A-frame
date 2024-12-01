from fastapi_users import schemas, models
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlalchemy import insert

from src.models.core_models import User as SUser
from src.utils.sqlalchemy_repository import SqlAlchemyRepository


class UsersRepository(SqlAlchemyRepository):
    model = SUser

    async def create(self,
                     user_create: schemas.UC,
                     safe: bool = False, 
                     user_id: str | None = None
                     ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_id:
        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        password_hash = PasswordHash((Argon2Hasher(),BcryptHasher(),))

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = password_hash.hash(password)
        if user_id is not None:
            user_dict["id"] = user_id

        async with self._session_factory as session:
            stmt = insert(self.model).values(**user_dict).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            created_user = res.scalar_one()

        return created_user
