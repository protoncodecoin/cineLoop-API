from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    username: str = Field(index=True, unique=True)
    email: str = Field(description="Enter valid email address", index=True, unique=True)
    password: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class PlayList(SQLModel, table=True):
    __tablename__ = "playlist"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    genre: str
    visibility: bool  # update it later to an enum type
    user_id: int = Field(foreign_key="user.id")


class UserPublic(SQLModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# sqlmodel_alembic_async/models.py
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = SQLModel.metadata
metadata.naming_convention = NAMING_CONVENTION
