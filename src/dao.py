from typing import Any, Dict

from sqlalchemy import asc, desc, func, insert, select
from sqlalchemy import delete as sql_delete
from sqlalchemy import update as sql_update

from src.schemas import PaginationParams, SortDirection, SortParams
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

    @classmethod
    def _get_sortable_fields(cls) -> set[str]:
        if not cls.model:
            return set()
        return {column.name for column in cls.model.__table__.columns}

    @classmethod
    def _validate_sort_field(cls, field: str) -> str:
        allowed_fields = cls._get_sortable_fields()
        if field not in allowed_fields:
            raise ValueError(
                f"Сортировка по полю '{field}' не разрешена. Доступные поля: {allowed_fields}"
            )
        return field

    @classmethod
    def _build_filters(cls, filters: Dict[str, Any]):
        conditions = []
        for key, value in filters.items():
            if value is None:
                continue

            if hasattr(cls.model, key):
                column = getattr(cls.model, key)
                if isinstance(value, str):
                    conditions.append(column.ilike(f"%{value}%"))
                else:
                    conditions.append(column == value)

        return conditions

    @classmethod
    async def find_with_pagination(
        cls, pagination: PaginationParams, sort: SortParams, **filters
    ) -> tuple[list, int]:
        async with async_session_maker() as session:
            sort_field = cls._validate_sort_field(sort.order_by)

            query = select(cls.model)

            filter_conditions = cls._build_filters(filters)
            if filter_conditions:
                query = query.where(*filter_conditions)

            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()

            sort_column = getattr(cls.model, sort_field)
            if sort.order_direction == SortDirection.DESC:
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            offset = (pagination.page - 1) * pagination.page_size
            query = query.offset(offset).limit(pagination.page_size)

            result = await session.execute(query)
            items = result.scalars().all()

            return items, total
