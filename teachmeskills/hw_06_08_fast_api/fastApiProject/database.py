from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declarative_base
# from models import Base
# Create an async engine for the SQLite database
engine = create_async_engine(
    'sqlite+aiosqlite:///database.db',
)

# Create a session factory for async sessions
LocalSession = async_sessionmaker(engine, expire_on_commit=False, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    """
    Base class for declarative models.
    """
    pass


async def create_tables():
    """
    Create all tables in the database.
    This function uses the metadata from the Base class.
    """
    async with engine.begin() as conn:
        a = Base.metadata
        print(a)
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
    """
    Drop all tables in the database.
    This function uses the metadata from the Base class.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def get_session() -> AsyncSession:
    """
    Get a new database session.
    This function is a dependency that can be used with FastAPI's dependency injection system.

    :return: AsyncSession instance
    """
    async with LocalSession() as session:
        yield session
