from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core.exceptions import NotFoundError
from models import ItemCreate, ItemPublic, ItemUpdate
from services import ItemService
from utils.dependencies import get_item_service

router = APIRouter()


@router.post("/", response_model=ItemPublic)
def create_item(
    item: ItemCreate,
    owner_id: int,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    return item_service.create_item(item, owner_id)


@router.get("/", response_model=list[ItemPublic])
def read_items(
    item_service: Annotated[ItemService, Depends(get_item_service)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return item_service.read_items(offset, limit)


@router.get("/{item_id}", response_model=ItemPublic)
def read_item(item_id: int, item_service: Annotated[ItemService, Depends(get_item_service)]):
    item = item_service.read_item(item_id)
    if not item:
        raise NotFoundError("Item", item_id)
    return item


@router.patch("/{item_id}", response_model=ItemPublic)
def update_item(
    item_id: int,
    item: ItemUpdate,
    item_service: Annotated[ItemService, Depends(get_item_service)],
):
    return item_service.update_item(item_id, item)


@router.delete("/{item_id}")
def delete_item(item_id: int, item_service: Annotated[ItemService, Depends(get_item_service)]):
    return item_service.delete_item(item_id)
