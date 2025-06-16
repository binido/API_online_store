from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class SUserCreate(BaseModel):
    email: EmailStr
    password: str


class SUserUpdate(BaseModel):
    email: Optional[EmailStr] = None


class SUserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
