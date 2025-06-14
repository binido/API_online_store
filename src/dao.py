from sqlalchemy import delete as sql_delete
from sqlalchemy import insert, select
from sqlalchemy import update as sql_update

from src.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(id=model_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def update(cls, model_id: int, **data):
        async with async_session_maker() as session:
            stmt = (
                sql_update(cls.model)
                .where(cls.model.id == model_id)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, model_id: int):
        async with async_session_maker() as session:
            stmt = (
                sql_delete(cls.model)
                .where(cls.model.id == model_id)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
