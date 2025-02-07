from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from core.database import get_session
from services import ItemService, UserService

SessionDep = Annotated[Session, Depends(get_session)]


def get_item_service(session: SessionDep) -> ItemService:
    return ItemService(session)


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)
