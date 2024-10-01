from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from src.auth.schemas import UserCreateSchema, UserSchema
from src.auth.services.repository import UserRepository

# Initialize password context with bcrypt hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher:
    """
    Service for hashing and verifying passwords.
    """

    @staticmethod
    async def hash_password(password: str) -> str:
        """
        Hash a plain password.

        :param password: Plain password
        :return: Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        :param plain_password: Plain password
        :param hashed_password: Hashed password
        :return: True if the password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)


class UserService:
    """
    Service for managing user operations.
    """

    def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher):
        """
        Initialize the service with a user repository and a password hasher.

        :param user_repo: Instance of UserRepository
        :param password_hasher: Instance of PasswordHasher
        """
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def create_user(self, data: UserCreateSchema, session: AsyncSession) -> User:
        """
        Create a new user.

        :param data: User creation schema
        :param session: Database session
        :return: Created user
        """
        user_dict = data.model_dump()
        user_dict['password'] = await self.password_hasher.hash_password(user_dict['password'])
        user = User(**user_dict)
        return await self.user_repo.add_user(user, session)

    async def authenticate_user(self, credentials: HTTPBasicCredentials, session: AsyncSession) -> User:
        """
        Authenticate a user based on credentials.

        :param credentials: HTTP basic credentials
        :param session: Database session
        :return: Authenticated user
        :raises HTTPException: If the user is not found or the password is incorrect
        """
        user = await self.user_repo.get_user_by_username(credentials.username, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not await self.password_hasher.verify_password(credentials.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user

    async def get_users(self, user_id: int, session: AsyncSession) -> list[UserSchema]:
        """
        Get a list of all users if the requesting user has admin privileges.

        :param user_id: ID of the requesting user
        :param session: Database session
        :return: List of users
        :raises HTTPException: If the requesting user is not an admin
        """
        user = await self.user_repo.get_user_by_id(user_id, session)
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Not enough privileges")
        users = await self.user_repo.get_all_users(session)
        return [UserSchema.model_validate(user) for user in users]
