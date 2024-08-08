from typing import Sequence

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User

# Initialize password context with bcrypt hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    """
    Repository for performing CRUD operations on User model.
    """

    @staticmethod
    async def add_user(user: User, session: AsyncSession) -> User:
        """
        Add a new user to the database.

        :param user: User instance to add
        :param session: Database session
        :return: Added user
        """
        session.add(user)
        await session.flush()
        await session.commit()
        return user

    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession) -> User:
        """
        Retrieve a user by their username.

        :param username: Username of the user
        :param session: Database session
        :return: User instance or None if not found
        """
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
        """
        Retrieve a user by their ID.

        :param user_id: ID of the user
        :param session: Database session
        :return: User instance or None if not found
        """
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_users(session: AsyncSession) -> Sequence[User]:
        """
        Retrieve all users from the database.

        :param session: Database session
        :return: Sequence of User instances
        """
        query = select(User)
        result = await session.execute(query)
        return result.scalars().all()
