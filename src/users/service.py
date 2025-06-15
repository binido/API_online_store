from typing import Optional

from fastapi import HTTPException, status

from src.schemas import PaginatedResponse, PaginationParams, SortParams

from .dao import UserDAO
from .schemas import SUserRead, SUserUpdate


async def get_user(user_id: int) -> Optional[SUserRead]:
    return await UserDAO.find_by_id(user_id)


async def list_users_paginated(
    pagination: PaginationParams,
    sort: SortParams,
    email: Optional[str] = None,
) -> PaginatedResponse[SUserRead]:
    filters = {}
    if email:
        filters["email"] = email

    items, total = await UserDAO.find_with_pagination(
        pagination=pagination, sort=sort, **filters
    )

    return PaginatedResponse.create(
        items=items, total=total, page=pagination.page, page_size=pagination.page_size
    )


async def update_user(user_id: int, schema: SUserUpdate) -> Optional[SUserRead]:
    user = await UserDAO.find_by_id(user_id)
    if not user:
        return None

    if schema.email and schema.email != user.email:
        existing_user = await UserDAO.find_by_email(schema.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует",
            )

    update_data = schema.model_dump(exclude_unset=True)
    if not update_data:
        return user

    return await UserDAO.update(user_id, **update_data)


async def delete_user(user_id: int, current_user_id: int) -> Optional[SUserRead]:
    if user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя удалить самого себя"
        )

    user = await UserDAO.find_by_id(user_id)
    if not user:
        return None

    return await UserDAO.delete(user_id)
