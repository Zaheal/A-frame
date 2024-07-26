from ..models.core_models import HouseModel
from ..utils.sqlalchemy_repository import SqlAlchemyRepository


class HousesRepository(SqlAlchemyRepository):
    model = HouseModel
