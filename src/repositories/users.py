from ..models.auth_models import User as SUser
from ..utils.sqlalchemy_repository import SqlAlchemyRepository


class UsersRepository(SqlAlchemyRepository):
    model = SUser
