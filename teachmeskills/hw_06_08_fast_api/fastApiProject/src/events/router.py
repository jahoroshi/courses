from typing import Annotated

from fastapi import APIRouter, Depends

from database import get_session
from src.auth.services import token_service
from src.events.schemas import EventShowSchema, EventBaseSchema, EventSubscriptionShowSchema, \
    EventSubscriptionBaseSchema
from src.events.services import event_service

# Initialize API router with prefix and tags
router = APIRouter(
    prefix="/events",
    tags=["🪩🫧🍸🥂🫧✧˖° Events"],
)


@router.post('', response_model=EventBaseSchema)
async def create(event: Annotated[EventBaseSchema, Depends()], current_user=Depends(token_service.get_current_user),
                 session=Depends(get_session, use_cache=True)):
    """
    Create a new event.

    :param event: Event creation schema
    :param current_user: Currently authenticated user
    :param session: Database session
    :return: Created event
    """
    return await event_service.create_event(event, current_user.id, session)


@router.get('', response_model=list[EventShowSchema])
async def get_events(session=Depends(get_session, use_cache=True)):
    """
    Retrieve a list of all upcoming events.

    :param session: Database session
    :return: List of events
    """
    return await event_service.list_events(session)


@router.post('/{event_id}', response_model=EventShowSchema)
async def subscription_to_event(event_id: int, current_user=Depends(token_service.get_current_user),
                                session=Depends(get_session, use_cache=True)):
    """
    Subscribe the current user to an event.

    :param event_id: ID of the event to subscribe to
    :param current_user: Currently authenticated user
    :param session: Database session
    :return: Updated event
    """
    return await event_service.subscribe_to_event(event_id, current_user.id, session)


@router.post('/subscribe/', response_model=EventSubscriptionShowSchema)
async def subscription_to_notification(notification_conf: EventSubscriptionBaseSchema,
                                       current_user=Depends(token_service.get_current_user),
                                       session=Depends(get_session, use_cache=True)):
    """
    Subscribe the current user to notifications for an event.

    This endpoint allows an authenticated user to subscribe to notifications for a specific event.
    Notifications will be sent according to the user's configuration.

    :param notification_conf: The notification configuration schema, including notification times.
    :param current_user: The currently authenticated user who is subscribing to notifications.
    :param session: Database session dependency.
    :return: The event subscription object with notification details.
    """
    return await event_service.subscribe_to_notifications(notification_conf, current_user.id, session)


@router.get('/my', response_model=list[EventShowSchema])
async def get_my(current_user=Depends(token_service.get_current_user), session=Depends(get_session, use_cache=True)):
    """
    Retrieve a list of events the current user is subscribed to.

    :param current_user: Currently authenticated user
    :param session: Database session
    :return: List of events the user is subscribed to
    """
    return await event_service.get_user_events(current_user.id, session)
