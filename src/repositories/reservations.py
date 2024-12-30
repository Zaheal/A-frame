from src.models.core_models import ReservationModel
from src.utils.sqlalchemy_repository import SqlAlchemyRepository


class ReservationsRepository(SqlAlchemyRepository):
    model = ReservationModel
