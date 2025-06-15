from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Номер страницы")
    page_size: int = Field(10, ge=1, le=100, description="Размер страницы")


class SortParams(BaseModel):
    order_by: str = Field("id", description="Поле для сортировки")
    order_direction: SortDirection = Field(
        SortDirection.ASC, description="Направление сортировки"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, items: list[T], total: int, page: int, page_size: int):
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )
