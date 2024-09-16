from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declarative_base
# from models import Base
# Create an async engine for the SQLite database
engine = create_async_engine(
    'postgresql+asyncpg://project1:123@db:5432/project1',
)


# Create a session factory for async sessions
LocalSession = async_sessionmaker(engine, expire_on_commit=False, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    """
    Base class for declarative models.
    """
    pass



async def get_session() -> AsyncSession:
    """
    Get a new database session.
    This function is a dependency that can be used with FastAPI's dependency injection system.

    :return: AsyncSession instance
    """
    async with LocalSession() as session:
        yield session
