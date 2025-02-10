from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.exceptions import NotFoundError
from core.logging import logger
from models import User, UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user (UserCreate): The user data to create.
        Returns:
            User: The created user.
        """
        try:
            db_user = User(**user.model_dump(exclude_unset=True))
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            logger.info(f"User created: {db_user}")
            return db_user
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    async def read_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        """
        Read a list of users.

        Args:
            offset (int, optional): The offset to start retrieving users from. Defaults to 0.
            limit (int, optional): The maximum number of users to retrieve. Defaults to 100.
        Returns:
            list[User]: The list of users retrieved.
        """
        try:
            query = select(User).order_by(User.id).offset(offset).limit(limit)
            result = await self.session.execute(query)
            users = result.scalars().all()
            logger.info(f"Users retrieved: {users}")
            return users
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve users: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    async def read_user(self, user_id: int) -> User | None:
        """
        Read a single user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.
        Returns:
            User | None: The user retrieved, or None if not found.
        """
        try:
            user = await self.session.get(User, user_id)
            if not user:
                logger.warning(f"User not found with ID: {user_id}")
                return None
            logger.info(f"User retrieved: {user}")
            return user
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """
        Update a user.

        Args:
            user_id (int): The ID of the user to update.
            user_update (UserUpdate): The updated user data.
        Returns:
            User: The updated user.
        """
        try:
            user_db = await self.session.get(User, user_id)
            if not user_db:
                logger.warning(f"User not found with ID: {user_id}")
                raise NotFoundError("User", user_id)
            user_data = user_update.model_dump(exclude_unset=True)
            for key, value in user_data.items():
                setattr(user_db, key, value)
            self.session.add(user_db)
            await self.session.commit()
            await self.session.refresh(user_db)
            logger.info(f"User updated: {user_db}")
            return user_db
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to update user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    async def delete_user(self, user_id: int) -> dict:
        """
        Delete a user.

        Args:
            user_id (int): The ID of the user to delete.
        Returns:
            dict: A dictionary indicating whether the user was deleted successfully.
        """
        try:
            user = await self.session.get(User, user_id)
            if not user:
                logger.warning(f"User not found with ID: {user_id}")
                raise NotFoundError("User", user_id)
            await self.session.delete(user)
            await self.session.commit()
            logger.info(f"User deleted with ID: {user_id}")
            return {"ok": True}
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to delete user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
