from src.models.core_models import HouseModel
from src.utils.sqlalchemy_repository import SqlAlchemyRepository


class HousesRepository(SqlAlchemyRepository):
    model = HouseModel
