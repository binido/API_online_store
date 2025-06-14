from fastapi import Query

from src.schemas import PaginationParams, SortDirection, SortParams


def get_pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)


def get_sort_params(
    order_by: str = Query("id"),
    order_direction: SortDirection = Query(
        SortDirection.ASC,
    ),
) -> SortParams:
    return SortParams(order_by=order_by, order_direction=order_direction)
