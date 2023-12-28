

from app.entities.todo import Todo
from app.services.database import Database


def get_all_items() -> list[Todo]:
    return Database.get_all_items()


def get_item_by_id(id: int) -> Todo:
    element = Database.get_item_by_id(id)
    if element is None:
        raise ValueError(f"Item with id {id} not found")
    return element


def create_item(item: Todo) -> dict:
    new_id = Database.create_item(item)
    return Database.get_item_by_id(new_id)


def update_item(id: int, new_item: Todo) -> dict:
    Database.update_item(id, new_item)
    return get_item_by_id(id)


def delete_item(id: int) -> bool:
    return Database.delete_item(id)
