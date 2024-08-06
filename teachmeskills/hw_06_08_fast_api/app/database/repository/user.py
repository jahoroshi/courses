from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from sqlalchemy import select

from app.database.db import new_session
from app.database.models import User
from app.schemas.user import UserCreateSchema, UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    @classmethod
    async def add(cls, data: UserCreateSchema) -> User:
        async with new_session() as session:
            user_dict = data.model_dump()
            user_dict['password'] = pwd_context.hash(user_dict['password'])
            user = User(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def __get_by_username(cls, username: str) -> User:
        async with new_session() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user

    @classmethod
    async def get_all(cls, credentials: HTTPBasicCredentials) -> list[UserSchema]:
        async with new_session() as session:
            user = await cls.authenticate(credentials)
            if not user.is_admin:
                raise HTTPException(status_code=403, detail="Not enough privileges")
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            return [UserSchema.model_validate(user) for user in users]

    @classmethod
    async def __verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def authenticate(cls, credentials: HTTPBasicCredentials) -> User | None:
        user = await cls.__get_by_username(credentials.username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not await cls.__verify_password(credentials.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
# # Пример проверки пароля
# stored_hashed_password = user.password  # Хешированный пароль из базы данных
# if verify_password(input_password, stored_hashed_password):
#     print("Пароль верный")
# else:
#     print("Пароль неверный")
