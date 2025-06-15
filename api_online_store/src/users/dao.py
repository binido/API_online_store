from src.dao import BaseDAO

from .models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_by_email(cls, email: str):
        return await cls.find_one_or_none(email=email)
