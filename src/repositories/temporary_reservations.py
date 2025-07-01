from sqlalchemy import insert, select, delete
from src.models.core_models import TemporaryReservationModel, User, ReservationModel
from src.schemas.base_schemas import SReservationAdd
from src.utils.sqlalchemy_repository import SqlAlchemyRepository


class TemporaryReservationsRepository(SqlAlchemyRepository):
    model = TemporaryReservationModel


    async def create(self, data: dict):
        async with self._session_factory as session:
            user_stmt = select(User.id).where(User.email == data['email'])
            result = await session.execute(user_stmt)
            user_id = result.scalar_one_or_none()

            if user_id:
                reservation_data = SReservationAdd(**data)
                filtered_data = reservation_data.model_dump()
                filtered_data['user_id'] = user_id
                stmt = insert(ReservationModel).values(**filtered_data).returning(ReservationModel)
            else:
                stmt = insert(self.model).values(**data).returning(self.model)

            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()


    async def delete_old_records(self,
                                 current_date):
        async with self._session_factory as session:
            await session.execute(delete(self.model).filter_by(self.model.end < current_date))
            await session.commit()