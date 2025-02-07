from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)  # type: ignore


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    email: str | None = None
    password: str | None = None
