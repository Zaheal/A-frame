from sqlalchemy import delete

from src.models.core_models import ReservationModel
from src.utils.sqlalchemy_repository import SqlAlchemyRepository


class ReservationsRepository(SqlAlchemyRepository):
    model = ReservationModel

    async def delete_old_records(self,
                                 current_date):
        async with self._session_factory as session:
            await session.execute(delete(self.model).filter_by(self.model.end < current_date))
            await session.commit()