from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Event

class EventRepository:
    """
    Repository for performing CRUD operations on Event model.
    """

    async def add_event(self, event: Event, session: AsyncSession) -> Event:
        """
        Add a new event to the database.

        :param event: Event instance to add
        :param session: Database session
        :return: Added event
        """
        session.add(event)
        await session.flush()
        await session.commit()
        return event

    async def get_list(self, session: AsyncSession) -> List[Event]:
        """
        Retrieve a list of upcoming events.

        :param session: Database session
        :return: List of events
        """
        query = select(Event).where(Event.meeting_time > datetime.now())
        result = await session.execute(query)
        return result.scalars().all()

    async def get_event_by_id(self, id: int, session: AsyncSession) -> Event:
        """
        Retrieve an event by its ID.

        :param id: ID of the event
        :param session: Database session
        :return: Event instance
        :raises HTTPException: If the event is not found
        """
        query = select(Event).where(Event.id == id)
        result = await session.execute(query)
        event = result.scalar_one_or_none()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    async def save_event(self, event: Event, session: AsyncSession) -> None:
        """
        Save changes to an existing event.

        :param event: Event instance to save
        :param session: Database session
        """
        session.add(event)
        await session.flush()
        await session.commit()
