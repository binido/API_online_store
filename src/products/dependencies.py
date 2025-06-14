from fastapi import HTTPException, Query

from src.schemas import SortDirection, SortParams


def get_product_sort_params(
    order_by: str = Query("id", description="Поля: id, name, price, created_at"),
    order_direction: SortDirection = Query(SortDirection.ASC),
) -> SortParams:
    allowed_fields = {"id", "name", "price", "created_at", "category_id"}
    if order_by not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое поле сортировки. Доступные: {allowed_fields}",
        )
    return SortParams(order_by=order_by, order_direction=order_direction)
