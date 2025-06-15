from typing import List, Optional

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import selectinload

from src.dao import BaseDAO
from src.database import async_session_maker
from src.schemas import SortDirection

from .models import Order, OrderItem


class OrderDAO(BaseDAO):
    model = Order

    @classmethod
    async def create_order_with_items(
        cls, user_id: int, items_data: List[dict]
    ) -> Order:
        async with async_session_maker() as session:
            order = Order(user_id=user_id)
            session.add(order)
            await session.flush()

            for item_data in items_data:
                order_item = OrderItem(order_id=order.id, **item_data)
                session.add(order_item)

            await session.commit()
            await session.refresh(order)

            return await cls.find_by_id_with_items(order.id)

    @classmethod
    async def find_by_id_with_items(cls, order_id: int) -> Optional[Order]:
        async with async_session_maker() as session:
            stmt = (
                select(cls.model)
                .options(selectinload(cls.model.items))
                .filter_by(id=order_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def find_user_orders_with_items(cls, user_id: int) -> List[Order]:
        async with async_session_maker() as session:
            stmt = (
                select(cls.model)
                .options(selectinload(cls.model.items))
                .filter_by(user_id=user_id)
                .order_by(cls.model.created_at.desc())
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def find_user_orders_paginated(
        cls, user_id: int, pagination, sort, status=None
    ):
        async with async_session_maker() as session:
            base_query = select(cls.model).filter(cls.model.user_id == user_id)
            if status:
                base_query = base_query.filter(cls.model.status == status)

            count_query = select(func.count()).select_from(base_query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()

            query = base_query.options(selectinload(cls.model.items))

            sort_field = cls._validate_sort_field(sort.order_by)
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


class OrderItemDAO(BaseDAO):
    model = OrderItem
