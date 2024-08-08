from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from src.auth.schemas import UserCreateSchema, UserSchema, TokenPairSchema, AccessTokenSchema, RefreshTokenSchema
from src.auth.services import user_service, token_service

# Initialize basic HTTP security
security = HTTPBasic()

# Initialize API router with prefix and tags
router = APIRouter(
    prefix="/auth",
    tags=["🗝️⋆｡ 𖦹°‧★ Authentication"],
)

@router.post("/users", response_model=UserSchema)
async def add_user(user: Annotated[UserCreateSchema, Depends()], session=Depends(get_session, use_cache=True)):
    """
    Add a new user.

    :param user: User creation schema
    :param session: Database session
    :return: Created user
    """
    return await user_service.create_user(user, session)

@router.get("/users", response_model=list[UserSchema])
async def get_users(current_user=Depends(token_service.get_current_user),
                    session=Depends(get_session, use_cache=True)):
    """
    Get a list of all users if the current user has admin privileges.

    :param current_user: Currently authenticated user
    :param session: Database session
    :return: List of users
    """
    return await user_service.get_users(current_user.id, session)

@router.post("/token", response_model=TokenPairSchema)
async def get_token_pair(user_data: OAuth2PasswordRequestForm = Depends(),
                         session=Depends(get_session, use_cache=True)):
    """
    Get a pair of JWT tokens (access and refresh) for the user.

    :param user_data: OAuth2 password request form containing username and password
    :param session: Database session
    :return: Token pair (access and refresh tokens)
    """
    credentials = HTTPBasicCredentials(username=user_data.username, password=user_data.password)
    user = await user_service.authenticate_user(credentials, session)
    return await token_service.create_jwt_token_pair(user_id=user.id)

@router.post("/token/refresh", response_model=AccessTokenSchema)
async def refresh_token(token: Annotated[RefreshTokenSchema, Depends()]):
    """
    Refresh the access token using a valid refresh token.

    :param token: Refresh token schema
    :return: New access token
    """
    return AccessTokenSchema(access_token=await token_service.refresh_access_token(token.refresh_token))

@router.post("/me", response_model=UserSchema)
async def get_me(current_user=Depends(token_service.get_current_user),
                 session: AsyncSession = Depends(get_session, use_cache=True)):
    """
    Get the currently authenticated user's details.

    :param current_user: Currently authenticated user
    :param session: Database session
    :return: User details
    """
    return await user_service.user_repo.get_user_by_id(current_user.id, session)
