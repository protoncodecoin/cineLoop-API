from sqlmodel import Field, SQLModel


class PlayList(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    genre: str
    visibility: bool  # update it later to an enum type
