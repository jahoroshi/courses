from fastapi.security import HTTPBasicCredentials

from app.database.models import User, Event
from app.database.repository.event import EventRepository
from app.database.repository.user import UserRepository
from app.schemas.event import EventBaseSchema
from app.schemas.user import UserCreateSchema, UserSchema


async def event_create(event: EventBaseSchema) -> Event:
    event = await EventRepository.add(event)
    return event

async def event_list() -> list[EventBaseSchema]:
    event = await EventRepository.get_list()
    return event

async def event_subscribe(event_id: int, credintials: HTTPBasicCredentials) -> Event:
    event = await EventRepository.subscribe(event_id, credintials)
    return event

async def get_my_events(credintials: HTTPBasicCredentials) -> list[EventBaseSchema]:
    event = await EventRepository.get_my_list(credintials)
    return event