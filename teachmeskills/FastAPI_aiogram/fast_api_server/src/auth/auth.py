import logging
import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer

from logger import logger
from models import User
from database import get_session

from dotenv import load_dotenv
load_dotenv()


# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain password matches the hashed password.

    Args:
    plain_password -- The plain text password entered by the user.
    hashed_password -- The hashed password stored in the database.

    Returns:
    bool -- True if passwords match, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
    password -- The plain text password to hash.

    Returns:
    str -- The hashed password.
    """
    return pwd_context.hash(password)


async def get_user(session: AsyncSession, username: str) -> Optional[User]:
    """
    Retrieves a user from the database by username.

    Args:
    session -- The active database session.
    username -- The username of the user to retrieve.

    Returns:
    User -- The user object if found, otherwise None.
    """
    logger.info(f"Fetching user: {username}")
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        logger.warning(f"User not found: {username}")
    return user


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
    """
    Authenticates a user by verifying the password.

    Args:
    session -- The active database session.
    username -- The username provided by the user.
    password -- The plain text password entered by the user.

    Returns:
    User -- The authenticated user if credentials are valid, otherwise False.
    """
    user = await get_user(session, username)
    if not user:
        logger.warning(f"Authentication failed for {username}: user not found")
        return False
    if not verify_password(password, user.password_hash):
        logger.warning(f"Authentication failed for {username}: incorrect password")
        return False
    logger.info(f"User authenticated: {username}")
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new access token.

    Args:
    data -- The payload to encode in the token.
    expires_delta -- Optional expiration time for the token.

    Returns:
    str -- The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Access token created for user: {data.get('sub')}")
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Creates a new refresh token.

    Args:
    data -- The payload to encode in the token.

    Returns:
    str -- The encoded JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Refresh token created for user: {data.get('sub')}")
    return encoded_jwt


async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    """
    Retrieves the current user based on the JWT token.

    Args:
    request -- The HTTP request containing the JWT token in headers or cookies.
    session -- The active database session.

    Returns:
    User -- The current user object if the token is valid, otherwise raises HTTPException.
    """
    token = None

    # First, check for the token in the Authorization header
    authorization: str = request.headers.get("Authorization")
    if authorization:
        scheme, _, param = authorization.partition(" ")
        if scheme.lower() != "bearer":
            logger.warning(f"Invalid authorization scheme: {scheme}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization scheme")
        token = param
    else:
        # If not found in headers, check the cookies (for web clients)
        token = request.cookies.get("access_token")
        if token:
            scheme, _, param = token.partition(" ")
            if scheme.lower() != "bearer":
                logger.warning("Invalid authorization scheme in cookie")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization scheme")
            token = param

    if not token:
        logger.warning("Token not provided")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not provided")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Username not found in token")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to get user from token")
    except JWTError:
        logger.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await get_user(session, username)
    if user is None:
        logger.warning(f"User not found for token: {username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    logger.info(f"User retrieved: {username}")
    return user
