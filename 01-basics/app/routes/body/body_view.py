from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import UUID4

from app.data.item_data import items
from app.models.item_model import ItemInput, ItemModel

router = APIRouter()


# * POST
@router.post("/item", status_code=status.HTTP_201_CREATED)
def create_item(
    inserted_model: ItemInput,
) -> ItemModel:
    item = ItemModel(**inserted_model.model_dump())
    items.append(item)
    return item


# * PUT
## Path + Quest Body
@router.put("/item/{id}")
async def update(
    id: UUID4,  # Path
    updated_data: ItemInput,  # request body
) -> ItemModel:
    "Using Path and Request body"
    found_item = next((item for item in items if item.id == id), None)
    if not found_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not exist"
        )
    found_item.modified_at = datetime.now()
    found_item.name = updated_data.name
    # No need to update in items list since found_item is a reference to the item in the list

    return found_item
