from ..schemas.base_schemas import SBusyTimeAdd, SBusyTimeEdit
from ..utils.unitofwork import IUnitOfWork


class BusyTimeService:
    async def add_busy_time(self, uow: IUnitOfWork, busy_time: SBusyTimeAdd):
        """

        :param uow:
        :param busy_time:
        :return:
        """
        busy_times_dict = busy_time.model_dump()
        async with uow:
            busy_time_id = await uow.busy_times.create(busy_times_dict)
            return busy_time_id

    async def get_busy_times(self, uow: IUnitOfWork, **filters):
        """

        :param uow:
        :return model:
        """
        async with uow:
            busy_times = await uow.busy_times.get_multi(**filters)
            return busy_times

    async def edit_busy_time(self, uow: IUnitOfWork, busy_time: SBusyTimeEdit, busy_time_id: int):
        """

        :param uow:
        :param busy_time_id:
        :param busy_time:
        :return busy_time_id:
        """
        busy_times_dict = busy_time.model_dump()
        async with uow:
            busy_time_id = await uow.busy_times.update(pk=busy_time_id, data=busy_times_dict)
            return busy_time_id

    async def remove_busy_time(self, uow: IUnitOfWork, busy_time_id: int):
        """

        :param uow:
        :param busy_time_id:
        :return:
        """
        async with uow:
            await uow.busy_times.delete(pk=busy_time_id)
            return
