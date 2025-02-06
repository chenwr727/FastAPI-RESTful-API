from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    title: str
    description: str | None = None


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")


class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = None
    description: str | None = None
