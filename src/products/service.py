from decimal import Decimal
from typing import Optional

from src.schemas import PaginatedResponse, PaginationParams, SortParams

from .dao import ProductDAO
from .schemas import SProductCreate, SProductRead, SProductUpdate


async def create_product(schema: SProductCreate) -> SProductRead:
    return await ProductDAO.add(**schema.model_dump())


async def get_product(product_id: int) -> Optional[SProductRead]:
    return await ProductDAO.find_by_id(product_id)


async def list_products_paginated(
    pagination: PaginationParams,
    sort: SortParams,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
) -> PaginatedResponse[SProductRead]:
    items, total = await ProductDAO.find_with_filters(
        pagination=pagination,
        sort=sort,
        name=name,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
    )

    return PaginatedResponse.create(
        items=items, total=total, page=pagination.page, page_size=pagination.page_size
    )


async def update_product(
    product_id: int, schema: SProductUpdate
) -> Optional[SProductRead]:
    return await ProductDAO.update(product_id, **schema.model_dump(exclude_unset=True))


async def delete_product(product_id: int) -> Optional[SProductRead]:
    return await ProductDAO.delete(product_id)
