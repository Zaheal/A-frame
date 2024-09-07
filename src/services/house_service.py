from src.schemas.base_schemas import SHouseAdd, SHouseEdit
from src.utils.unitofwork import IUnitOfWork


class HouseService:
    async def add_house(self, uow: IUnitOfWork, house: SHouseAdd):
        """

        :param uow:
        :param house:
        :return:
        """
        houses_dict = house.model_dump()
        async with uow:
            house_id = await uow.houses.create(houses_dict)
            return house_id

    async def get_houses(self, uow: IUnitOfWork):
        """

        :param uow:
        :return model:
        """
        async with uow:
            houses = await uow.houses.get_multi()
            return houses

    async def edit_house(self, uow: IUnitOfWork, house: SHouseEdit, house_id: int):
        """

        :param uow:
        :param house_id:
        :param house:
        :return house_id:
        """
        houses_dict = house.model_dump()
        async with uow:
            house_id = await uow.houses.update(pk=house_id, data=houses_dict)
            return house_id

    async def remove_house(self, uow: IUnitOfWork, house_id: int):
        """

        :param uow:
        :param house_id:
        :return:
        """
        async with uow:
            await uow.houses.delete(id=house_id)
            return

    async def get_house(self, uow: IUnitOfWork, house_id: int):
        async with uow:
            res = await uow.houses.get_single(id=house_id)
            return res
