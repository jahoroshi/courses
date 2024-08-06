from sqlalchemy import select

from app.database.db import new_session
from app.schemas import STaskAdd, STask
from app.database.models import TaskORM


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_shcemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_shcemas