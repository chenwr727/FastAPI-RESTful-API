from sqlmodel import Session, select

from core.exceptions import NotFoundError
from core.logging import logger
from models import Item, ItemCreate, ItemUpdate, User


class ItemService:
    def __init__(self, session: Session):
        self.session = session

    def create_item(self, item: ItemCreate, owner_id: int) -> Item:
        """
        Create a new item.

        Args:
            item (ItemCreate): The item to create.
            owner_id (int): The ID of the owner of the item.
        Returns:
            Item: The created item.
        """
        owner = self.session.get(User, owner_id)
        if not owner:
            logger.warning(f"User not found with ID: {owner_id}")
            raise NotFoundError("User", owner_id)

        db_item = Item(owner_id=owner_id, **item.model_dump(exclude_unset=True))
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        logger.info(f"Item created: {db_item}")
        return db_item

    def read_items(self, offset: int = 0, limit: int = 100) -> list[Item]:
        """
        Retrieve a list of items.

        Args:
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The limit for pagination. Defaults to 100.
        Returns:
            list[Item]: A list of items.
        """
        items = self.session.exec(
            select(Item).order_by(Item.id).offset(offset).limit(limit)
        ).all()
        logger.info(f"Items retrieved: {items}")
        return items

    def read_item(self, item_id: int) -> Item | None:
        """
        Retrieve an item by ID.

        Args:
            item_id (int): The ID of the item to retrieve.
        Returns:
            Item | None: The item if found, otherwise None.
        """
        item = self.session.get(Item, item_id)
        if not item:
            logger.warning(f"Item not found with ID: {item_id}")
        else:
            logger.info(f"Item retrieved: {item}")
        return item

    def update_item(self, item_id: int, item: ItemUpdate) -> Item:
        """
        Update an item.

        Args:
            item_id (int): The ID of the item to update.
            item (ItemUpdate): The updated item data.
        Returns:
            Item: The updated item.
        """
        item_db = self.session.get(Item, item_id)
        if not item_db:
            logger.warning(f"Item not found with ID: {item_id}")
            raise NotFoundError("Item", item_id)
        item_data = item.model_dump(exclude_unset=True)
        for key, value in item_data.items():
            setattr(item_db, key, value)
        self.session.add(item_db)
        self.session.commit()
        self.session.refresh(item_db)
        logger.info(f"Item updated: {item_db}")
        return item_db

    def delete_item(self, item_id: int) -> dict:
        """
        Delete a item.

        Args:
            item_id (int): The ID of the item to delete.
        Returns:
            dict: A dictionary indicating the success of the deletion.
        """
        item = self.session.get(Item, item_id)
        if not item:
            logger.warning(f"Item not found with ID: {item_id}")
            raise NotFoundError("Item", item_id)
        self.session.delete(item)
        self.session.commit()
        logger.info(f"Item deleted with ID: {item_id}")
        return {"ok": True}
