from typing import Annotated
from fastapi import APIRouter, Query
from sqlmodel import select

from .authentication import user_dependency

from ..models import PlayList, User
from ..database import SessionDep


router = APIRouter(
    tags=["playlist"],
    prefix="/playlists",
)


@router.post("/")
async def create_playlist(
    playlist: PlayList,
    session: SessionDep,
    token: Annotated[User, user_dependency],
    current_user: Annotated[User, user_dependency],
) -> PlayList:
    session.add(playlist)
    session.commit()

    session.refresh(playlist)

    return playlist


@router.get("/")
async def get_playlist(
    session: SessionDep,
    current_user: Annotated[User, user_dependency],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[PlayList]:
    """Get All playlist"""
    statement = select(PlayList).offset(offset).limit(limit)
    playlists = session.exec(statement).all()

    return playlists
