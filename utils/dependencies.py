from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from services import ItemService, UserService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_item_service(session: AsyncSessionDep) -> ItemService:
    """
    Dependency to get an ItemService instance with an AsyncSession.

    Args:
        session (AsyncSession): The async database session.

    Returns:
        ItemService: An instance of ItemService.
    """
    return ItemService(session)


def get_user_service(session: AsyncSessionDep) -> UserService:
    """
    Dependency to get a UserService instance with an AsyncSession.

    Args:
        session (AsyncSession): The async database session.

    Returns:
        UserService: An instance of UserService.
    """
    return UserService(session)
