from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.db import delete_tables, create_tables
from app.handlers.user import router as user_router
from app.handlers.events import router as event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    print('Base is cleared and ready.')
    yield
    print('Shutdown complete.')


app = FastAPI(lifespan=lifespan)
app.include_router(event_router)
app.include_router(user_router)

