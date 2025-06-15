from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies import get_pagination_params
from src.schemas import PaginatedResponse, PaginationParams, SortParams

from .dependencies import get_product_sort_params
from .schemas import SProductCreate, SProductRead, SProductUpdate
from .service import (
    create_product,
    delete_product,
    get_product,
    list_products_paginated,
    update_product,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_view(schema: SProductCreate) -> SProductRead:
    return await create_product(schema)


@router.get("/")
async def get_products_view(
    pagination: PaginationParams = Depends(get_pagination_params),
    sort: SortParams = Depends(get_product_sort_params),
    name: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[Decimal] = Query(None),
    max_price: Optional[Decimal] = Query(None),
) -> PaginatedResponse[SProductRead]:
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400, detail="Минимальная цена не может быть больше максимальной"
        )

    return await list_products_paginated(
        pagination=pagination,
        sort=sort,
        name=name,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
    )


@router.get("/{product_id}")
async def get_product_view(product_id: int) -> SProductRead:
    product = await get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{product_id}")
async def update_product_view(product_id: int, schema: SProductUpdate) -> SProductRead:
    product = await update_product(product_id, schema)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_view(product_id: int) -> None:
    product = await delete_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
