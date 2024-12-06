from contextlib import asynccontextmanager

from fastapi import FastAPI
from .database import create_db_and_tables


from .routers import playlists, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(playlists.router)
app.include_router(users.router)


@app.get("/")
async def index():
    return {"message": "Welcome to the cineloop API v1"}


# @app.post("/playlist")
# async def create_playlist(playlist: PlayList, session: SessionDep) -> PlayList:
#     session.add(playlist)
#     session.commit()
#     session.refresh(playlist)

#     return playlist


# @app.get("/playlist")
# async def get_playlist(
#     session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
# ) -> list[PlayList]:
#     playlists = session.exec(select(PlayList).offset(offset).limit(limit)).all()

#     return playlists
