from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Event
from src.auth.services import user_service
from src.events.schemas import EventShowSchema, EventBaseSchema
from src.events.services.repository import EventRepository

class EventService:
    """
    Service for managing events.
    """

    def __init__(self, event_repo: EventRepository):
        """
        Initialize the service with an event repository.

        :param event_repo: Instance of EventRepository
        """
        self.event_repo = event_repo

    async def create_event(self, event: EventBaseSchema, user_id: int, session: AsyncSession) -> Event:
        """
        Create a new event and associate it with a user.

        :param event: Event creation schema
        :param user_id: ID of the user creating the event
        :param session: Database session
        :return: Created event
        :raises HTTPException: If an event with the same name already exists
        """
        event_dict = event.model_dump()
        user = await user_service.user_repo.get_user_by_id(user_id, session)
        event_dict.update({'users': [user]})
        event = Event(**event_dict)
        try:
            created_event = await self.event_repo.add_event(event, session)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Event with this name already exists"
            )
        return created_event

    async def list_events(self, session: AsyncSession) -> List[EventShowSchema]:
        """
        List all events.

        :param session: Database session
        :return: List of events
        """
        events = await self.event_repo.get_list(session)
        return [EventShowSchema.model_validate(event) for event in events]

    async def subscribe_to_event(self, event_id: int, user_id: int, session: AsyncSession) -> Event:
        """
        Subscribe a user to an event.

        :param event_id: ID of the event
        :param user_id: ID of the user
        :param session: Database session
        :return: Updated event
        :raises HTTPException: If the event's meeting time is in the past or if the user is already subscribed
        """
        user = await user_service.user_repo.get_user_by_id(user_id, session)
        event = await self.event_repo.get_event_by_id(event_id, session)
        if event.meeting_time <= datetime.now():
            raise HTTPException(status_code=404, detail="Meeting time is in the past")
        if user in event.users:
            raise HTTPException(status_code=409, detail="User already subscribed to the event")
        event.users.append(user)
        await self.event_repo.save_event(event, session)
        return event

    async def get_user_events(self, user_id: int, session: AsyncSession) -> List[EventShowSchema]:
        """
        Get events a user is subscribed to.

        :param user_id: ID of the user
        :param session: Database session
        :return: List of events the user is subscribed to
        """
        query = select(Event).where(Event.users.any(id=user_id))
        result = await session.execute(query)
        events = result.scalars().all()
        return [EventShowSchema.model_validate(event) for event in events]
