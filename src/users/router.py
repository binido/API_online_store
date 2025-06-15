from fastapi import APIRouter, Depends

from src.dependencies import get_current_user
from src.users.models import User
from src.users.schemas import SUserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=SUserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
