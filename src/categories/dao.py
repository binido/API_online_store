from src.dao import BaseDAO
from .models import Category


class CategoryDAO(BaseDAO):
    model = Category
