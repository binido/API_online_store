from datetime import datetime

from pydantic import BaseModel


class SCategoryCreate(BaseModel):
    name: str
    description: str | None = None


class SCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class SCategoryRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
