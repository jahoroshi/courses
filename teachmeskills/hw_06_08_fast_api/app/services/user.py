from fastapi.security import HTTPBasicCredentials

from app.database.models import User
from app.database.repository.user import UserRepository
from app.schemas.user import UserCreateSchema, UserSchema


async def create_user(data: UserCreateSchema) -> User:
    user = await UserRepository.add(data)
    return user


async def users(credintials: HTTPBasicCredentials) -> list[UserSchema]:
    user_all = await UserRepository.get_all(credintials)
    return user_all
