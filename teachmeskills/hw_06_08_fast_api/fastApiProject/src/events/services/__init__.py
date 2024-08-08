from src.events.services.repository import EventRepository
from src.events.services.management import EventService

event_repository = EventRepository()
event_service = EventService(event_repository)
