from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.entities.todo import Todo
from app.todo_app import get_all_items, get_item_by_id, create_item, update_item, delete_item

openapi_tag = {
    "name": "Todo app",
    "description": "Manage todos - CRUD operations",
    "externalDocs": {
        "description": "Items external docs",
        "url": "https://fastapi.tiangolo.com/",
    },
}

router = APIRouter(
    prefix="/todo",
    tags=[openapi_tag["name"]],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=[openapi_tag["name"]], status_code=status.HTTP_200_OK)
async def route_get_all_items() -> list[Todo]:
    return await get_all_items()


@router.get("/{id}", tags=[openapi_tag["name"]], status_code=status.HTTP_200_OK)
async def route_get_item_by_id(id: int) -> Todo:
    try:
        return await get_item_by_id(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post("/", tags=[openapi_tag["name"]], status_code=status.HTTP_201_CREATED)
async def route_create_item(item: Todo) -> Todo:
    try:
        return await create_item(item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put("/{id}", tags=[openapi_tag["name"]], status_code=status.HTTP_200_OK)
async def route_update_item(id: int, new_item: Todo) -> Todo:
    try:
        return await update_item(id, new_item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{id}", tags=[openapi_tag["name"]], status_code=status.HTTP_204_NO_CONTENT)
async def route_delete_item(id: int):
    try:
        await delete_item(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
