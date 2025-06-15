from datetime import datetime

from pydantic import BaseModel, EmailStr


class SUserCreate(BaseModel):
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUserRead(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class SToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
