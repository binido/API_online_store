from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class SProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category_id: int = Field(..., gt=0)


class SProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category_id: Optional[int] = Field(None, gt=0)


class SProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    category_id: int
    created_at: datetime

    class Config:
        orm_mode = True
