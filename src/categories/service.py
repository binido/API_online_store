from .dao import CategoryDAO
from .schemas import SCategoryCreate, SCategoryUpdate


async def create_category(schema: SCategoryCreate):
    return await CategoryDAO.add(**schema.model_dump())


async def get_category(category_id: int):
    return await CategoryDAO.find_by_id(category_id)


async def list_categories():
    return await CategoryDAO.find_all()


async def update_category(category_id: int, schema: SCategoryUpdate):
    return await CategoryDAO.update(
        category_id, **schema.model_dump(exclude_unset=True)
    )


async def delete_category(category_id: int):
    return await CategoryDAO.delete(category_id)
