from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Query
from sqlmodel import select
from .db import create_db_and_tables, SessionDep
from .models import PlayList


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"message": "Welcome to the cineloop API v1"}


@app.post("/playlist")
async def create_playlist(playlist: PlayList, session: SessionDep) -> PlayList:
    session.add(playlist)
    session.commit()
    session.refresh(playlist)

    return playlist


@app.get("/playlist")
async def get_playlist(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[PlayList]:
    playlists = session.exec(select(PlayList).offset(offset).limit(limit)).all()

    return playlists
