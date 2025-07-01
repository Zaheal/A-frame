from src.schemas.base_schemas import STemporaryReservationAdd, STemporaryReservationEdit
from src.utils.unitofwork import IUnitOfWork


class TemporaryReservationService:
    async def add_temporary_reservation(self,
                                        uow: IUnitOfWork,
                                        reservation: STemporaryReservationAdd):
        """
        Записывает бронь без зарегестрированного пользователя

        :param uow:
        :param reservation:
        :return:
        """
        reservations_dict = reservation.model_dump()
        async with uow:
            try:
                reservation = await uow.temporary_reservations.create(reservations_dict)
                return reservation
            except Exception as e:
                raise e
    
    
    async def get_by_email(self,
                           uow: IUnitOfWork,
                           email: str):
        """
        Выдает всю бронь с определенной почтой
        
        :param uow:
        :param email:
        :return:
        """
        async with uow:
            try:
                reservation_data = await uow.temporary_reservations.get_multi(email=email)
                return reservation_data
            except Exception as e:
                raise e


    async def get_reservations(self,
                               uow: IUnitOfWork,
                               **filters):
        """
        Список временной брони
        
        :param uow:
        :return:
        """
        async with uow:
            reservations = await uow.temporary_reservations.get_multi(**filters)
            return reservations


    async def edit_temporary_reservation(self, 
                                         uow: IUnitOfWork, 
                                         reservation: STemporaryReservationEdit, 
                                         reservation_id: int):
        """
        Редактирует бронь и возвращает её

        :param uow:
        :param reservation_id:
        :param reservation:
        :return reservation_data:
        """
        reservations_dict = reservation.model_dump()
        async with uow:
            reservation_data = await uow.temporary_reservations.update(pk=reservation_id, data=reservations_dict)
            return reservation_data
        

    async def remove_temporary_reservation(self, 
                                           uow: IUnitOfWork, 
                                           reservation_id: int):
        """
        Удаляет бронь из базы данных

        :param uow:
        :param reservation_id:
        :return:
        """
        async with uow: 
            return await uow.temporary_reservations.delete(id=reservation_id)


    async def remove_old_reservations(self,
                                  uow: IUnitOfWork,
                                  current_date):
        """
        
        :uow:
        :current_date:
        """
        async with uow:
            await uow.reservations.delete_old_records(current_date)