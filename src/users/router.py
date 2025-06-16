from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies import get_current_user
from src.schemas import PaginatedResponse, PaginationParams, SortParams
from src.users import service
from src.users.models import User
from src.users.schemas import SUserRead, SUserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=SUserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("", response_model=PaginatedResponse[SUserRead])
async def get_users(
    pagination: PaginationParams = Depends(),
    sort: SortParams = Depends(),
    email: str = Query(None, description="Фильтр по email"),
):
    return await service.list_users_paginated(
        pagination=pagination, sort=sort, email=email
    )


@router.get("/{user_id}", response_model=SUserRead)
async def get_user(user_id: int):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


@router.put("/{user_id}", response_model=SUserRead)
async def update_user(user_id: int, user_data: SUserUpdate):
    user = await service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    user = await service.delete_user(user_id, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return {"message": "Пользователь успешно удален"}
