import os
from datetime import timedelta, datetime, UTC

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import User
from src.auth.schemas import TokenPairSchema

# Initialize OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Set secret key and algorithm for JWT
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default-i9i3902849209323m009sfhs90dh")
ALGORITHM = "HS512"
USER_IDENTIFIER = "user_id"

# Define expiration times for access and refresh tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24 * 7

class TokenService:
    """
    Service for managing JWT tokens.
    """

    async def create_jwt_token_pair(self, user_id: int) -> TokenPairSchema:
        """
        Create a pair of JWT tokens (access and refresh).

        :param user_id: ID of the user
        :return: TokenPairSchema containing access and refresh tokens
        """
        access_token = await self._create_jwt_token(
            {USER_IDENTIFIER: user_id, "type": "access"},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        refresh_token = await self._create_jwt_token(
            {USER_IDENTIFIER: user_id, "type": "refresh"},
            timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS),
        )

        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, refresh_token: str) -> str:
        """
        Refresh the access token using a valid refresh token.

        :param refresh_token: The refresh token
        :return: New access token
        """
        payload = await self._get_token_payload(refresh_token, "refresh")

        return await self._create_jwt_token(
            {USER_IDENTIFIER: payload[USER_IDENTIFIER], "type": "access"},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    async def _create_jwt_token(self, data: dict, delta: timedelta) -> str:
        """
        Create a JWT token.

        :param data: Data to encode in the token
        :param delta: Expiration time delta
        :return: Encoded JWT token
        """
        expires_delta = datetime.now(UTC) + delta
        data.update({"exp": expires_delta})
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def _get_token_payload(self, token: str, token_type: str) -> dict:
        """
        Decode and validate a JWT token.

        :param token: JWT token
        :param token_type: Expected type of the token ("access" or "refresh")
        :return: Decoded payload
        :raises HTTPException: If the token is invalid
        """
        try:
            payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        if payload.get("type") != token_type:
            raise HTTPException(status_code=401, detail="Invalid token")
        if payload.get(USER_IDENTIFIER) is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        return payload

    async def get_current_user(self, token: str = Depends(oauth2_scheme),
                               session: AsyncSession = Depends(get_session, use_cache=True)) -> User:
        """
        Get the current user based on the access token.

        :param token: Access token
        :param session: Database session
        :return: User object
        :raises HTTPException: If the token is invalid or user not found
        """
        payload = await self._get_token_payload(token, "access")
        try:
            query = select(User).where(User.id == payload[USER_IDENTIFIER])
            result = await session.execute(query)
            result.unique()
            return result.scalar_one()
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
