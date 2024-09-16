import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.auth.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_user
)
from database import get_session
from logger import logger
from models import User
from src.auth.schemas import UserRead, UserCreate, Token, RefreshTokenRequest, TelegramLink

from dotenv import load_dotenv
load_dotenv()


# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(tags=["auth"])

# Create a new user with hashed password
@router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user_obj = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
    )
    session.add(user_obj)
    try:
        await session.commit()
        await session.refresh(user_obj)
        logger.info(f"New user created: {user.username}")
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail="Error creating user")
    return user_obj

# Get current authenticated user information
@router.get("/users/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# Login user and generate access and refresh tokens
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}
    )
    logger.info(f"User {user.username} successfully logged in")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Refresh access token using refresh token
@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    token_request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session)
):
    refresh_token = token_request.refresh_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.info(f"Invalid username in token: {username}")
            raise credentials_exception
    except JWTError:
        logger.info(f"Error verifying refresh token: {refresh_token}")
        raise credentials_exception
    user = await get_user(session, username)
    if user is None:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user.username}
    )
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# Link Telegram account to the current authenticated user
@router.post("/link_telegram", response_model=UserRead)
async def link_telegram_account(
    data: TelegramLink,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    current_user.telegram_id = data.telegram_id
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return current_user

# Get token by Telegram ID if the user is linked to Telegram
@router.post("/get_token_by_telegram", response_model=Token)
async def get_token_by_telegram(data: TelegramLink, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.telegram_id == data.telegram_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found or not linked to Telegram")

    # Generate new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
