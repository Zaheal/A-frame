from abc import ABC, abstractmethod
from typing import Type

from src.repositories.houses import HousesRepository
from src.repositories.reservations import ReservationsRepository
from src.repositories.users import UsersRepository
from src.repositories.temporary_reservations import TemporaryReservationsRepository
from src.database.db import db_helper


class IUnitOfWork(ABC):
    houses: Type[HousesRepository]
    reservations: Type[ReservationsRepository]
    users: Type[UsersRepository]
    temporary_reservations: Type[TemporaryReservationsRepository]

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
        self.reservations = ReservationsRepository(self.session)
        self.temporary_reservations = TemporaryReservationsRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
