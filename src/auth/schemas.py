from pydantic import BaseModel, EmailStr


class SUserCreate(BaseModel):
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
