

from app.entities.todo import Todo
from app.services.database import Database


async def get_all_items() -> list[Todo]:
    database = Database()
    return await database.get_all_items()


async def get_item_by_id(id: int) -> Todo:
    database = Database()
    element = await database.get_item_by_id(id)
    if element is None:
        raise ValueError(f"Item with id {id} not found")
    return element


async def create_item(item: Todo) -> dict:
    database = Database()
    new_id = await database.create_item(item)
    return await database.get_item_by_id(new_id)


async def update_item(id: int, new_item: Todo) -> dict:
    database = Database()
    await database.update_item(id, new_item)
    return await get_item_by_id(id)


async def delete_item(id: int) -> bool:
    database = Database()
    return await database.delete_item(id)
