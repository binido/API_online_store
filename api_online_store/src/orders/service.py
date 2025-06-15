from typing import Optional

from fastapi import HTTPException, status

from src.products.dao import ProductDAO
from src.schemas import PaginatedResponse, PaginationParams, SortParams

from .dao import OrderDAO
from .models import OrderStatus
from .schemas import SOrderCreate, SOrderRead


async def create_order(user_id: int, schema: SOrderCreate) -> SOrderRead:
    items_data = []

    for item in schema.items:
        product = await ProductDAO.find_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товар с ID {item.product_id} не найден",
            )

        items_data.append(
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_order_time": product.price,
            }
        )

    order = await OrderDAO.create_order_with_items(user_id, items_data)
    return order


async def get_user_order(user_id: int, order_id: int) -> Optional[SOrderRead]:
    order = await OrderDAO.find_by_id_with_items(order_id)
    if not order:
        return None

    if order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Доступ к заказу запрещен"
        )

    return order


async def list_user_orders_paginated(
    user_id: int,
    pagination: PaginationParams,
    sort: SortParams,
    status: Optional[OrderStatus] = None,
) -> PaginatedResponse[SOrderRead]:
    items, total = await OrderDAO.find_user_orders_paginated(
        user_id=user_id, pagination=pagination, sort=sort, status=status
    )

    return PaginatedResponse.create(
        items=items, total=total, page=pagination.page, page_size=pagination.page_size
    )


async def cancel_user_order(user_id: int, order_id: int) -> Optional[SOrderRead]:
    order = await OrderDAO.find_by_id(order_id)
    if not order:
        return None

    if order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Доступ к заказу запрещен"
        )

    if order.status == OrderStatus.cancelled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Заказ уже отменен"
        )

    updated_order = await OrderDAO.update(order_id, status=OrderStatus.cancelled)
    return await OrderDAO.find_by_id_with_items(updated_order.id)


async def update_order_status_by_payment_service(
    order_id: int, status: OrderStatus
) -> Optional[SOrderRead]:
    order = await OrderDAO.find_by_id(order_id)
    if not order:
        return None

    updated_order = await OrderDAO.update(order_id, status=status)
    return await OrderDAO.find_by_id_with_items(updated_order.id)
