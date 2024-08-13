from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Event, Notification


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

    async def create_or_update_notification(self, notification: Notification, event: Event, user_id: int,
                                            session: AsyncSession) -> Notification:
        """
        Create or update a notification for a user and event.

        If a notification for the given event and user already exists, update it with the new details.
        Otherwise, create a new notification.

        :param notification: Notification instance to create or update
        :param event: Event instance associated with the notification
        :param user_id: ID of the user associated with the notification
        :param session: Database session
        :return: The updated or newly created notification
        """

        # Query to find existing notification for the user and event
        query = select(Notification).where(
            (Notification.event_id == event.id) & (Notification.user_id == user_id))
        result = await session.execute(query)
        existing_notif = result.scalar_one_or_none()

        if existing_notif:
            # Update the existing notification with new details
            existing_notif.first_notif_id = notification.first_notif_id
            existing_notif.second_notif_id = notification.second_notif_id
            existing_notif.first_notification = notification.first_notification
            existing_notif.second_notification = notification.second_notification
        else:
            # Add the new notification to the session
            session.add(notification)

        # Save changes to the database
        await session.flush()
        await session.commit()

        # Return the updated or newly created notification
        return existing_notif or notification

