from abc import ABC, abstractmethod
from typing import Type

from ..database.db import db_helper
from ..repositories.houses import HousesRepository
from ..repositories.busy_times import BusyTimesRepository
from ..repositories.users import UsersRepository


class IUnitOfWork(ABC):
    houses: Type[HousesRepository]
    busy_times: Type[BusyTimesRepository]
    users: Type[UsersRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self._session_factory = db_helper.session_factory

    async def __aenter__(self):
        self.session = self._session_factory()

        self.users = UsersRepository(self.session)
        self.houses = HousesRepository(self.session)
        self.busy_times = BusyTimesRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
