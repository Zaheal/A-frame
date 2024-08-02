from ..models.core_models import ReservationModel
from ..utils.sqlalchemy_repository import SqlAlchemyRepository


class ReservationsRepository(SqlAlchemyRepository):
    model = ReservationModel
