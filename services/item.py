from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.exceptions import NotFoundError
from core.logging import logger
from models import Item, ItemCreate, ItemUpdate, User


class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(self, item: ItemCreate, owner_id: int) -> Item:
        """
        Create a new item.

        Args:
            item (ItemCreate): The item to create.
            owner_id (int): The ID of the owner of the item.
        Returns:
            Item: The created item.
        """
        try:
            owner = await self.session.get(User, owner_id)
            if not owner:
                logger.warning(f"User not found with ID: {owner_id}")
                raise NotFoundError("User", owner_id)

            db_item = Item(owner_id=owner_id, **item.model_dump(exclude_unset=True))
            self.session.add(db_item)
            await self.session.commit()
            await self.session.refresh(db_item)
            logger.info(f"Item created: {db_item}")
            return db_item
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to create item: {e}")
            raise

    async def read_items(self, offset: int = 0, limit: int = 100) -> list[Item]:
        """
        Retrieve a list of items.

        Args:
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The limit for pagination. Defaults to 100.
        Returns:
            list[Item]: A list of items.
        """
        try:
            query = select(Item).order_by(Item.id).offset(offset).limit(limit)
            result = await self.session.execute(query)
            items = result.scalars().all()
            logger.info(f"Items retrieved: {items}")
            return items
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve items: {e}")
            raise

    async def read_item(self, item_id: int) -> Item | None:
        """
        Retrieve an item by ID.

        Args:
            item_id (int): The ID of the item to retrieve.
        Returns:
            Item | None: The item if found, otherwise None.
        """
        try:
            item = await self.session.get(Item, item_id)
            if not item:
                logger.warning(f"Item not found with ID: {item_id}")
            else:
                logger.info(f"Item retrieved: {item}")
            return item
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve item: {e}")
            raise

    async def update_item(self, item_id: int, item: ItemUpdate) -> Item:
        """
        Update an item.

        Args:
            item_id (int): The ID of the item to update.
            item (ItemUpdate): The updated item data.
        Returns:
            Item: The updated item.
        """
        try:
            item_db = await self.session.get(Item, item_id)
            if not item_db:
                logger.warning(f"Item not found with ID: {item_id}")
                raise NotFoundError("Item", item_id)

            item_data = item.model_dump(exclude_unset=True)
            for key, value in item_data.items():
                setattr(item_db, key, value)
            self.session.add(item_db)
            await self.session.commit()
            await self.session.refresh(item_db)
            logger.info(f"Item updated: {item_db}")
            return item_db
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to update item: {e}")
            raise

    async def delete_item(self, item_id: int) -> dict:
        """
        Delete an item.

        Args:
            item_id (int): The ID of the item to delete.
        Returns:
            dict: A dictionary indicating the success of the deletion.
        """
        try:
            item = await self.session.get(Item, item_id)
            if not item:
                logger.warning(f"Item not found with ID: {item_id}")
                raise NotFoundError("Item", item_id)

            await self.session.delete(item)
            await self.session.commit()
            logger.info(f"Item deleted with ID: {item_id}")
            return {"ok": True}
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to delete item: {e}")
            raise
