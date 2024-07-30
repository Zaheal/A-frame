from pydantic import BaseModel
from sqlalchemy import delete, select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, db_session: AsyncSession):
        self._session_factory = db_session

    async def create(self, data: dict) -> int:
        async with self._session_factory as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update(self, pk: int, data: dict) -> int:
        async with self._session_factory as session:
            stmt = update(self.model).values(**data).filter_by(id=pk).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> None:
        async with self._session_factory as session:
            await session.execute(delete(self.model).filter_by(**filters))
            await session.commit()

    async def get_single(self, **filters) -> BaseModel | None:
        async with self._session_factory as session:
            stmt = select(self.model).filter_by(**filters)
            row = await session.execute(stmt)
            return row.scalar_one_or_none()

    async def get_multi(self, **filters) -> list[BaseModel]:
        async with self._session_factory as session:
            stmt = select(self.model).filter_by(**filters).order_by('id').limit(100)
            res = await session.execute(stmt)
            return res.unique().scalars().all()
