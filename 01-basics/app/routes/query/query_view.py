from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import UUID4

from app.data.item_data import items
from app.models.item_model import ItemModel

router = APIRouter()


# # * POST
# @router.post("/create", status_code=status.HTTP_201_CREATED)
# def create_item(
#     inserted_model: ItemInput = Query(),
# ) -> ItemModel:
#     item = ItemModel(**inserted_model.model_dump())
#     items.append(item)
#     return item


# * GET
@router.get("/all")
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


# # * PUT
# @router.put("/update")
# async def update(
#     updated_data: ItemInput,
#     id: UUID4 = Query(),
# ) -> ItemModel:
#     found_item = next((item for item in items if item.id == id), None)
#     if not found_item:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not exist"
#         )
#     found_item.modified_at = datetime.now()
#     found_item.name = updated_data.name
#     # No need to update in items list since found_item is a reference to the item in the list

#     return found_item


# * DELETE
@router.delete(
    "/delete",
    # "/delete/{id}",
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
