from sqlmodel import Session, select

from core.exceptions import NotFoundError
from core.logging import logger
from models import User, UserCreate, UserUpdate


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserCreate) -> User:
        """
        Create a new user

        Args:
            user (UserCreate): The user data to create
        Returns:
            User: The created user
        """
        db_user = User(**user.model_dump(exclude_unset=True))
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        logger.info(f"User created: {db_user}")
        return db_user

    def read_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        """
        Read a list of users

        Args:
            offset (int, optional): The offset to start retrieving users from. Defaults to 0.
            limit (int, optional): The maximum number of users to retrieve. Defaults to 100.
        Returns:
            list[User]: The list of users retrieved
        """
        users = self.session.exec(select(User).order_by(User.id).offset(offset).limit(limit)).all()
        logger.info(f"Users retrieved: {users}")
        return users

    def read_user(self, user_id: int) -> User | None:
        """
        Read a single user by ID

        Args:
            user_id (int): The ID of the user to retrieve
        Returns:
            User | None: The user retrieved, or None if not found
        """
        user = self.session.get(User, user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
        else:
            logger.info(f"User retrieved: {user}")
        return user

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        """
        Uopdate a user

        Args:
            user_id (int): The ID of the user to update
            user (UserUpdate): The updated user data
        Returns:
            User: The updated user
        """
        user_db = self.session.get(User, user_id)
        if not user_db:
            logger.warning(f"User not found with ID: {user_id}")
            raise NotFoundError("User", user_id)
        user_data = user.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user_db, key, value)
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        logger.info(f"User updated: {user_db}")
        return user_db

    def delete_user(self, user_id: int) -> dict:
        """
        Delete a user

        Args:
            user_id (int): The ID of the user to delete
        Returns:
            dict: A dictionary indicating whether the user was deleted successfully
        """
        user = self.session.get(User, user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            raise NotFoundError("User", user_id)
        self.session.delete(user)
        self.session.commit()
        logger.info(f"User deleted with ID: {user_id}")
        return {"ok": True}
