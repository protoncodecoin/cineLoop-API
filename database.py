from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from . import models  # noqa: F401

# sqlite_file_name = "cineloop.db"
sqlite_url = "sqlite:///./cineloop/cineloop.db"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """Create the database and tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
