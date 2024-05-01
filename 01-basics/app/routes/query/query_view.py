from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import UUID4

from app.data.item_data import items
from app.models.item_model import ItemModel

router = APIRouter()


# * GET
@router.get("/items/all")
async def get_all(
    limit: Optional[int] = Query(default=100, ge=0),
) -> list[ItemModel]:
    return items[:limit]


@router.get("/item")
async def get_one(id: UUID4 = Query()) -> ItemModel:
    found_item = next((item for item in items if item.id == id), None)
    if not found_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not exist"
        )
    return found_item


# * DELETE
@router.delete(
    "/item",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(id: UUID4 = Query()) -> None:
    found_item = next((item for item in items if item.id == id), None)
    if not found_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not exist"
        )
    items.remove(found_item)
    return None
