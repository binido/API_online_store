from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies import get_current_user
from src.schemas import PaginatedResponse, PaginationParams, SortParams
from src.users.models import User

from . import service
from .models import OrderStatus
from .schemas import SOrderCreate, SOrderRead, SOrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/all", response_model=PaginatedResponse[SOrderRead])
async def get_all_orders(
    pagination: PaginationParams = Depends(),
    sort: SortParams = Depends(),
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
):
    return await service.list_all_orders_paginated(
        pagination=pagination, sort=sort, status=status_filter
    )


@router.get("/all/{order_id}", response_model=SOrderRead)
async def get_order(order_id: int):
    order = await service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден"
        )
    return order


@router.patch("/all/{order_id}", response_model=SOrderRead)
async def update_order_view(order_id: int, schema: SOrderUpdate):
    order = await service.update_order(order_id, status=schema.status)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.delete("/all/{order_id}", response_model=SOrderRead)
async def delete_order_view(order_id: int):
    order = await service.delete_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден"
        )
    return order


@router.post("", response_model=SOrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: SOrderCreate, current_user: User = Depends(get_current_user)
):
    return await service.create_order(current_user.id, order_data)


@router.get("", response_model=PaginatedResponse[SOrderRead])
async def get_my_orders(
    pagination: PaginationParams = Depends(),
    sort: SortParams = Depends(),
    status_filter: Optional[OrderStatus] = Query(
        None, alias="status", description="Фильтр по статусу"
    ),
    current_user: User = Depends(get_current_user),
):
    return await service.list_user_orders_paginated(
        user_id=current_user.id, pagination=pagination, sort=sort, status=status_filter
    )


@router.get("/{order_id}", response_model=SOrderRead)
async def get_my_order(order_id: int, current_user: User = Depends(get_current_user)):
    order = await service.get_user_order(current_user.id, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден"
        )
    return order


@router.patch("/{order_id}/cancel", response_model=SOrderRead)
async def cancel_my_order(
    order_id: int, current_user: User = Depends(get_current_user)
):
    order = await service.cancel_user_order(current_user.id, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден"
        )
    return order
