from typing import List

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy import select
from datetime import datetime

from sqlalchemy.orm import selectinload

from app.database.db import new_session
from app.database.models import Event
from app.database.repository.user import UserRepository
from app.schemas.event import EventBaseSchema


class EventRepository:
    @classmethod
    async def add(cls, event: EventBaseSchema) -> Event:
        async with new_session() as session:
            event_dict = event.model_dump()
            event = Event(**event_dict)
            session.add(event)
            await session.flush()
            await session.commit()
            return event

    @classmethod
    async def get_list(cls) -> List[EventBaseSchema]:
        async with new_session() as session:
            query = select(Event).where(Event.meeting_time > datetime.now())
            result = await session.execute(query)
            events = result.scalars().all()
            return [EventBaseSchema.model_validate(event) for event in events]

    @classmethod
    async def __get_by_id(cls, id: int) -> Event:
        async with new_session() as session:
            query = select(Event).where(Event.id == id)
            result = await session.execute(query)
            event = result.scalar_one_or_none()
            if not event:
                raise HTTPException(status_code=404, detail="Event not found")
            return event

    @classmethod
    async def subscribe(cls, event_id: int, credintials: HTTPBasicCredentials) -> Event:
        user = await UserRepository.authenticate(credintials)
        event = await cls.__get_by_id(event_id)
        event.users.append(user)
        async with new_session() as session:
            session.add(event)
            await session.flush()
            await session.commit()
        return event

    @classmethod
    async def get_my_list(cls, credintials: HTTPBasicCredentials) -> List[EventBaseSchema]:
        user = await UserRepository.authenticate(credintials)
        async with new_session() as session:
            query = (
                select(Event)
                .join(Event.users)
                .options(selectinload(Event.users))
                .where(Event.users.any(id=user.id))
            )
            result = await session.execute(query)
            events = result.scalars().all()
            return [EventBaseSchema.model_validate(event) for event in events]


