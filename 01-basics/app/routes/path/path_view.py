from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import UUID4

from app.data.item_data import items
from app.models.item_model import ItemModel

router = APIRouter()


@router.get("/items/{id}")
async def get_one(
    id: Annotated[UUID4, Path(title="The Id of the item to get", min_length=1)],
    # id: UUID4,
) -> ItemModel:
    found_item = next((item for item in items if item.id == id), None)
    if not found_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not exist"
        )
    return found_item


# * DELETE
@router.delete(
    "/items/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_item(
    id: Annotated[UUID4, Path(title="The ID of the item to delete")],
) -> None:
    found_item = next((item for item in items if item.id == id), None)
    if not found_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not exist"
        )
    items.remove(found_item)
    return None
