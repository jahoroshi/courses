from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from src.auth.router import router as user_router
from src.events.router import router as event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for handling application lifespan events.

    This function sets up the database by creating tables at startup and prints status messages.

    :param app: FastAPI application instance
    """
    # Uncomment the next line if you want to delete tables before creating them
    # await delete_tables()

    # Create all tables in the database
    await create_tables()
    print('Base is cleared and ready.')

    yield  # Yield control back to the application

    print('Shutdown complete.')


# Create the FastAPI application with the custom lifespan context manager
app = FastAPI(lifespan=lifespan)

# Include the event router with a prefix
app.include_router(event_router, prefix='/api/v1')

# Include the user router with a prefix
app.include_router(user_router, prefix='/api/v1')


