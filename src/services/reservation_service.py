import uuid
from typing import Optional

from src.schemas.base_schemas import SReservationAdd, SReservationEdit, SReservation
from src.utils.unitofwork import IUnitOfWork


class ReservationService:
    async def add_reservation(self, uow: IUnitOfWork, reservation: SReservationAdd, user_id: uuid.UUID):
        """
        Записывает бронь в базу данных и возвращает id брони

        :param user_id:
        :param uow:
        :param reservation:
        :return:
        """
        reservations_dict = reservation.model_dump()
        reservations_dict['user_id'] = user_id
        async with uow:
            try:
                reservation_id = await uow.reservations.create(reservations_dict)
                return reservation_id
            except Exception as e:
                raise e

    async def get_reservations(self, uow: IUnitOfWork, **filters) -> list[SReservation]:
        """
        Возвращает список отфильтрованной брони (отсутствие фильтра, тоже фильтр)

        :param uow:
        :return model:
        """
        async with uow:
            reservations = await uow.reservations.get_multi(**filters)
            return reservations

    async def edit_reservation(self, uow: IUnitOfWork, reservation: SReservationEdit, reservation_id: int):
        """
        Редактирует бронь и возвращает её

        :param uow:
        :param reservation_id:
        :param reservation:
        :return reservation_data:
        """
        reservations_dict = reservation.model_dump()
        async with uow:
            reservation_data = await uow.reservations.update(pk=reservation_id, data=reservations_dict)
            return reservation_data

    async def remove_reservation(self, uow: IUnitOfWork, reservation_id: int, user_id: Optional[uuid.UUID] | None = None):
        """
        Удаляет бронь из базы данных

        :param user_id:
        :param uow:
        :param reservation_id:
        :return:
        """
        async with uow:
            if user_id:
                return await uow.reservations.delete(id=reservation_id, user_id=user_id)
            else:  
                return await uow.reservations.delete(id=reservation_id)

