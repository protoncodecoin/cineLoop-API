from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select


from ..database import SessionDep
from ..models import User, UserPublic, UserCreate, Token
from ..utilities import hash_pass
from .authentication import create_access_token


router = APIRouter(
    tags=["users"],
    prefix="/users",
)


def authenticate_user(db_session: SessionDep, username: str, password: str):
    statement = select(User).where(User.username == username)
    user_obj = db_session.exec(statement).first()

    if not user_obj:
        return False
    if not hash_pass.verify_password(password, user_obj.password):
        return False

    return user_obj


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: SessionDep
) -> Token:
    user_obj = authenticate_user(db_session, form_data.username, form_data.password)

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user_obj.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/", response_model=list[UserPublic], status_code=status.HTTP_200_OK)
async def get_users(
    db_session: SessionDep, offset: int = 0, limit: int = Query(default=100, le=100)
) -> list[UserPublic]:
    """Get all users"""
    statement = select(User).offset(offset).limit(limit)
    users = db_session.exec(statement).all()
    return users


@router.get("/{user_id}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_user(db_session: SessionDep, user_id: int) -> UserPublic:
    """Get user by ID"""
    statement = select(User).where(User.id == user_id)
    user = db_session.exec(statement).first()

    if user is None:
        raise HTTPException(
            detail="User is not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db_session: SessionDep, user_id: int):
    """Delete User by ID"""
    statement = select(User).where(User.id == user_id)
    user = db_session.exec(statement).first()

    if user is None:
        raise HTTPException(
            detail="User is not found", status_code=status.HTTP_404_NOT_FOUND
        )
    db_session.delete(user)
    db_session.commit()

    return None


@router.post("/", response_model=UserPublic)
async def create_user(db_session: SessionDep, user: UserCreate) -> UserPublic:
    """Create a new user"""
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=hash_pass.get_password_hash(user.password),
        id=None,
    )
    try:
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        return new_user

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The data sent is invalid or malformed",
        )
