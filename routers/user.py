from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core.exceptions import NotFoundError
from models import UserCreate, UserPublic, UserUpdate
from services import UserService
from utils.dependencies import get_user_service

router = APIRouter()


@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(user)


@router.get("/", response_model=list[UserPublic])
def read_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return user_service.read_users(offset, limit)


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = user_service.read_user(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserUpdate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.delete_user(user_id)
