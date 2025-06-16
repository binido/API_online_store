from sqlalchemy import Column, DateTime, Integer, String, func

from src.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
