from typing import Annotated

from fastapi import APIRouter, Depends

from app.database.repository.repository import TaskRepository
from app.schemas import STaskAdd, STask, STaskID

router = APIRouter(
    prefix="/user",
    tags=["☻ user"],
)
@router.post("")
async def add_task(
        task: Annotated[STaskAdd, Depends()],
) -> STaskID:
    task_id = await TaskRepository.add_one(task)
    return {'ok': True, 'task_id': task_id}


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks
