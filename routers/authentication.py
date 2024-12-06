from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import select

from ..models import TokenData, User, UserPublic
from ..database import SessionDep


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY: str = "d9d7eb04b8cb355b3f636b5178322acd712540c45df187758f2a93f635b28192"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def get_user(
    username: str,
):  # TODO: -> Fix bug ( Session.exec() missing 1 required positional argument: 'statement')
    """Get user from the database"""
    statement = select(User).where(User.username == username)
    user_obj = SessionDep.exec(statement)

    if user_obj:
        return UserPublic(**user_obj)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get current user using token data"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


SECRET_KEY: str = "d9d7eb04b8cb355b3f636b5178322acd712540c45df187758f2a93f635b28192"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create access token for user"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


user_dependency = Depends(get_current_user)
