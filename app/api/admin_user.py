from datetime import timedelta
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.crud.admin_user import create_admin_user, get_admin_user
from app.db.db import get_db
from app.auth.auth import Token, authenticate_user, create_access_token, get_current_active_user, get_password_hash
from app.schemas.admin_user import AdminUser, AdminUserInDB
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/admin_user",
    tags=["admin_user"],
)


@router.post("/token")
async def login_for_access_token(
    db: Annotated[Session, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@router.post("/create_user", response_model=bool)
async def create_user(
    _: Annotated[AdminUser, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    username: str,
    email: str,
    password: str,
):
    user = get_admin_user(db, username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    hashed_password = get_password_hash(password)
    user = AdminUserInDB(username=username, hashed_password=hashed_password, email=email)
    user = create_admin_user(db, user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user",
        )
    return True
