from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field

from .models import OrderStatus


class SOrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="ID товара")
    quantity: int = Field(..., gt=0, description="Количество")


class SOrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_order_time: Decimal

    class Config:
        from_attributes = True


class SOrderCreate(BaseModel):
    items: List[SOrderItemCreate] = Field(
        ..., min_items=1, description="Список товаров"
    )


class SOrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime
    items: List[SOrderItemRead]

    class Config:
        from_attributes = True


class SOrderUpdate(BaseModel):
    status: OrderStatus
