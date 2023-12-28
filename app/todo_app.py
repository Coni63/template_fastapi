

from app.entities.todo import Todo
from app.services.database import Database


async def get_all_items() -> list[Todo]:
    return await Database.get_all_items()


async def get_item_by_id(id: int) -> Todo:
    element = await Database.get_item_by_id(id)
    if element is None:
        raise ValueError(f"Item with id {id} not found")
    return element


async def create_item(item: Todo) -> dict:
    new_id = await Database.create_item(item)
    return await Database.get_item_by_id(new_id)


async def update_item(id: int, new_item: Todo) -> dict:
    await Database.update_item(id, new_item)
    return await get_item_by_id(id)


async def delete_item(id: int) -> bool:
    return await Database.delete_item(id)
