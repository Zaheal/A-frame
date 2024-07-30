import uuid
from typing import Optional

from starlette.status import HTTP_403_FORBIDDEN

from ..schemas.base_schemas import SBusyTimeAdd, SBusyTimeEdit, SBusyTime
from ..utils.unitofwork import IUnitOfWork
from ..auth.user import current_superuser


class BusyTimeService:
    async def add_busy_time(self, uow: IUnitOfWork, busy_time: SBusyTimeAdd, user_id: uuid.UUID) -> int:
        """
        Записывает бронь в базу данных и возвращает id брони

        :param user_id:
        :param uow:
        :param busy_time:
        :return:
        """
        busy_times_dict = busy_time.model_dump()
        busy_times_dict['user_id'] = user_id
        async with uow:
            try:
                busy_time_id = await uow.busy_times.create(busy_times_dict)
                return busy_time_id
            except Exception as e:
                raise e

    async def get_busy_times(self, uow: IUnitOfWork, **filters) -> list[SBusyTime]:
        """
        Возвращает список отфильтрованной брони (отсутствие фильтра, тоже фильтр)

        :param uow:
        :return model:
        """
        async with uow:
            busy_times = await uow.busy_times.get_multi(**filters)
            return busy_times

    async def edit_busy_time(self, uow: IUnitOfWork, busy_time: SBusyTimeEdit, busy_time_id: int) -> int:
        """
        Редактирует бронь и возвращает её id

        :param uow:
        :param busy_time_id:
        :param busy_time:
        :return busy_time_id:
        """
        busy_times_dict = busy_time.model_dump()
        async with uow:
            busy_time_id = await uow.busy_times.update(pk=busy_time_id, data=busy_times_dict)
            return busy_time_id

    async def remove_busy_time(self, uow: IUnitOfWork, busy_time_id: int, user_id: Optional[uuid.UUID] = None) -> None:
        """
        Удаляет бронь из базы данных

        :param user_id:
        :param uow:
        :param busy_time_id:
        :return:
        """
        async with uow:
            try:
                current_superuser()
            except HTTP_403_FORBIDDEN as _:  # выполнится если пользователь обычный обыватель
                await uow.busy_times.delete(id=busy_time_id, user_id=user_id)
                return
            else:  # выполнится если пользователь админ
                await uow.busy_times.delete(id=busy_time_id)
                return
