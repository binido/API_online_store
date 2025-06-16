from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.utils import verify_token
from src.schemas import PaginationParams, SortDirection, SortParams
from src.users.dao import UserDAO

security = HTTPBearer()


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


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(token.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserDAO.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
