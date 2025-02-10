from typing import Annotated, Dict, List, Optional

from fastapi import APIRouter, Depends, Query

from core.exceptions import NotFoundError
from core.response import StandardResponse
from models import ItemCreate, ItemPublic, ItemUpdate
from services import ItemService
from utils.dependencies import get_item_service

router = APIRouter()


@router.post("/", response_model=StandardResponse[ItemPublic])
async def create_item(
    item: ItemCreate,
    owner_id: int,
    item_service: Annotated[ItemService, Depends(get_item_service)],
) -> StandardResponse[ItemPublic]:
    """
    Create a new item.

    Args:
        item (ItemCreate): The item data to create.
        owner_id (int): The ID of the item owner.
        item_service (ItemService): Dependency injected item service.
    Returns:
        StandardResponse[ItemPublic]: A standardized response containing the created item.
    """
    new_item = await item_service.create_item(item, owner_id)
    return StandardResponse(status="success", message="Item created successfully", data=new_item)


@router.get("/", response_model=StandardResponse[List[ItemPublic]])
async def read_items(
    item_service: Annotated[ItemService, Depends(get_item_service)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> StandardResponse[List[ItemPublic]]:
    """
    Read a list of items.

    Args:
        item_service (ItemService): Dependency injected item service.
        offset (int, optional): The offset to start retrieving items from. Defaults to 0.
        limit (int, optional): The maximum number of items to retrieve. Defaults to 100.
    Returns:
        StandardResponse[List[ItemPublic]]: A standardized response containing the list of items.
    """
    items = await item_service.read_items(offset, limit)
    return StandardResponse(status="success", message="Items retrieved successfully", data=items)


@router.get("/{item_id}", response_model=StandardResponse[Optional[ItemPublic]])
async def read_item(
    item_id: int,
    item_service: Annotated[ItemService, Depends(get_item_service)],
) -> StandardResponse[Optional[ItemPublic]]:
    """
    Read a single item by ID.

    Args:
        item_id (int): The ID of the item to retrieve.
        item_service (ItemService): Dependency injected item service.
    Returns:
        StandardResponse[Optional[ItemPublic]]: A standardized response containing the item.
    """
    item = await item_service.read_item(item_id)
    if not item:
        raise NotFoundError("Item", item_id)
    return StandardResponse(status="success", message="Item retrieved successfully", data=item)


@router.patch("/{item_id}", response_model=StandardResponse[ItemPublic])
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    item_service: Annotated[ItemService, Depends(get_item_service)],
) -> StandardResponse[ItemPublic]:
    """
    Update an item.

    Args:
        item_id (int): The ID of the item to update.
        item_update (ItemUpdate): The updated item data.
        item_service (ItemService): Dependency injected item service.
    Returns:
        StandardResponse[ItemPublic]: A standardized response containing the updated item.
    """
    updated_item = await item_service.update_item(item_id, item_update)
    return StandardResponse(status="success", message="Item updated successfully", data=updated_item)


@router.delete("/{item_id}", response_model=StandardResponse[Dict[str, bool]])
async def delete_item(
    item_id: int,
    item_service: Annotated[ItemService, Depends(get_item_service)],
) -> StandardResponse[Dict[str, bool]]:
    """
    Delete an item.

    Args:
        item_id (int): The ID of the item to delete.
        item_service (ItemService): Dependency injected item service.
    Returns:
        StandardResponse[Dict[str, bool]]: A standardized response indicating success.
    """
    result = await item_service.delete_item(item_id)
    return StandardResponse(status="success", message="Item deleted successfully", data=result)
