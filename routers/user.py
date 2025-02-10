from typing import Annotated, Dict, List, Optional

from fastapi import APIRouter, Depends, Query

from core.exceptions import NotFoundError
from core.response import StandardResponse
from models import UserCreate, UserPublic, UserUpdate
from services import UserService
from utils.dependencies import get_user_service

router = APIRouter()


@router.post("/", response_model=StandardResponse[UserPublic])
async def create_user(
    user: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> StandardResponse[UserPublic]:
    """
    Create a new user.

    Args:
        user (UserCreate): The user data to create.
        user_service (UserService): Dependency injected user service.
    Returns:
        StandardResponse[UserPublic]: A standardized response containing the created user.
    """
    new_user = await user_service.create_user(user)
    return StandardResponse(status="success", message="User created successfully", data=new_user)


@router.get("/", response_model=StandardResponse[List[UserPublic]])
async def read_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> StandardResponse[List[UserPublic]]:
    """
    Read a list of users.

    Args:
        user_service (UserService): Dependency injected user service.
        offset (int, optional): The offset to start retrieving users from. Defaults to 0.
        limit (int, optional): The maximum number of users to retrieve. Defaults to 100.
    Returns:
        StandardResponse[List[UserPublic]]: A standardized response containing the list of users.
    """
    users = await user_service.read_users(offset, limit)
    return StandardResponse(status="success", message="Users retrieved successfully", data=users)


@router.get("/{user_id}", response_model=StandardResponse[Optional[UserPublic]])
async def read_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> StandardResponse[Optional[UserPublic]]:
    """
    Read a single user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        user_service (UserService): Dependency injected user service.
    Returns:
        StandardResponse[Optional[UserPublic]]: A standardized response containing the user.
    """
    user = await user_service.read_user(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return StandardResponse(status="success", message="User retrieved successfully", data=user)


@router.patch("/{user_id}", response_model=StandardResponse[UserPublic])
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> StandardResponse[UserPublic]:
    """
    Update a user.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The updated user data.
        user_service (UserService): Dependency injected user service.
    Returns:
        StandardResponse[UserPublic]: A standardized response containing the updated user.
    """
    updated_user = await user_service.update_user(user_id, user_update)
    return StandardResponse(status="success", message="User updated successfully", data=updated_user)


@router.delete("/{user_id}", response_model=StandardResponse[Dict[str, bool]])
async def delete_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> StandardResponse[Dict[str, bool]]:
    """
    Delete a user.

    Args:
        user_id (int): The ID of the user to delete.
        user_service (UserService): Dependency injected user service.
    Returns:
        StandardResponse[Dict[str, bool]]: A standardized response indicating success.
    """
    result = await user_service.delete_user(user_id)
    return StandardResponse(status="success", message="User deleted successfully", data=result)
