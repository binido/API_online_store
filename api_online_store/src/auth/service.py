from datetime import timedelta

from fastapi import HTTPException, status

from src.config import settings
from src.users.dao import UserDAO
from src.users.schemas import SUserRead

from .schemas import SToken, SUserCreate, SUserLogin
from .utils import (
    create_access_token,
    get_password_hash,
    verify_password,
)


async def register_user(user_data: SUserCreate) -> SUserRead:
    existing_user = await UserDAO.find_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    hashed_password = get_password_hash(user_data.password)
    user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    return user


async def authenticate_user(login_data: SUserLogin) -> SToken:
    user = await UserDAO.find_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )

    return SToken(access_token=access_token)
