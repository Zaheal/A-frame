from ..models.core_models import BusyTimeModel
from ..utils.sqlalchemy_repository import SqlAlchemyRepository


class BusyTimesRepository(SqlAlchemyRepository):
    model = BusyTimeModel
