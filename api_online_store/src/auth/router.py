from fastapi import APIRouter, status

from src.users.schemas import SUserRead

from .schemas import SToken, SUserCreate, SUserLogin
from .service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: SUserCreate) -> SUserRead:
    return await register_user(user_data)


@router.post("/login", response_model=SToken)
async def login(login_data: SUserLogin) -> SToken:
    return await authenticate_user(login_data)
