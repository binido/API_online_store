from decimal import Decimal
from typing import Optional

from sqlalchemy import and_

from src.dao import BaseDAO
from src.database import async_session_maker
from src.schemas import PaginationParams, SortParams

from .models import Product


class ProductDAO(BaseDAO):
    model = Product

    @classmethod
    def _get_sortable_fields(cls) -> set[str]:
        base_fields = super()._get_sortable_fields()
        return base_fields | {"price"}

    @classmethod
    async def find_with_filters(
        cls,
        pagination: PaginationParams,
        sort: SortParams,
        name: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
    ) -> tuple[list, int]:
        base_filters = {}
        if name:
            base_filters["name"] = name
        if category_id:
            base_filters["category_id"] = category_id

        if min_price is None and max_price is None:
            return await cls.find_with_pagination(
                pagination=pagination, sort=sort, **base_filters
            )

        async with async_session_maker() as session:
            from sqlalchemy import asc, desc, func, select

            sort_field = cls._validate_sort_field(sort.order_by)

            query = select(cls.model)

            filter_conditions = cls._build_filters(base_filters)

            if min_price is not None:
                filter_conditions.append(cls.model.price >= min_price)
            if max_price is not None:
                filter_conditions.append(cls.model.price <= max_price)

            if filter_conditions:
                query = query.where(and_(*filter_conditions))

            count_query = select(func.count()).select_from(query.subquery())
            total_result = await session.execute(count_query)
            total = total_result.scalar()

            sort_column = getattr(cls.model, sort_field)
            if sort.order_direction.value == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            offset = (pagination.page - 1) * pagination.page_size
            query = query.offset(offset).limit(pagination.page_size)

            result = await session.execute(query)
            items = result.scalars().all()

            return items, total
