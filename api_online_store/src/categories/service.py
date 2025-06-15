from typing import Optional

from src.schemas import PaginatedResponse, PaginationParams, SortParams

from .dao import CategoryDAO
from .schemas import SCategoryCreate, SCategoryRead, SCategoryUpdate


async def create_category(schema: SCategoryCreate):
    return await CategoryDAO.add(**schema.model_dump())


async def get_category(category_id: int):
    return await CategoryDAO.find_by_id(category_id)


async def list_categories():
    return await CategoryDAO.find_all()


async def update_category(category_id: int, schema: SCategoryUpdate):
    return await CategoryDAO.update(
        category_id, **schema.model_dump(exclude_unset=True)
    )


async def delete_category(category_id: int):
    return await CategoryDAO.delete(category_id)


async def list_categories_paginated(
    pagination: PaginationParams, sort: SortParams, name: Optional[str] = None
) -> PaginatedResponse[SCategoryRead]:
    filters = {}
    if name:
        filters["name"] = name

    items, total = await CategoryDAO.find_with_pagination(
        pagination=pagination, sort=sort, **filters
    )

    return PaginatedResponse.create(
        items=items, total=total, page=pagination.page, page_size=pagination.page_size
    )
