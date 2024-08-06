from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy.exc import IntegrityError

from app.database.repository.repository import TaskRepository
from app.schemas import STask
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.user import create_user, users

security = HTTPBasic()

router = APIRouter(
    prefix="/auth",
    tags=["☻ user"],
)


@router.post("/user", response_model=UserSchema)
async def user_create(user: Annotated[UserCreateSchema, Depends()]):
    try:
        return await create_user(user)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="User already exists")


@router.get("/user/all", response_model=list[UserSchema])
async def get_users(credentials: HTTPBasicCredentials = Depends(security)):
    return await users(credentials)
