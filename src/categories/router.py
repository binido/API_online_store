from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies import get_pagination_params, get_sort_params
from src.schemas import PaginatedResponse, PaginationParams, SortParams

from .schemas import SCategoryCreate, SCategoryRead, SCategoryUpdate
from .service import (
    create_category,
    delete_category,
    get_category,
    list_categories_paginated,
    update_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=PaginatedResponse[SCategoryRead])
async def get_categories_view(
    pagination: PaginationParams = Depends(get_pagination_params),
    sort: SortParams = Depends(get_sort_params),
    name: Optional[str] = Query(None, description="Фильтр по названию"),
) -> PaginatedResponse[SCategoryRead]:
    return await list_categories_paginated(pagination=pagination, sort=sort, name=name)


@router.post("/", response_model=SCategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category_view(schema: SCategoryCreate) -> SCategoryRead:
    return await create_category(schema)


@router.get("/{category_id}", response_model=SCategoryRead)
async def get_category_view(category_id: int) -> SCategoryRead:
    category = await get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=SCategoryRead)
async def update_category_view(
    category_id: int, schema: SCategoryUpdate
) -> SCategoryRead:
    category = await update_category(category_id, schema)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_view(category_id: int) -> None:
    category = await delete_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
