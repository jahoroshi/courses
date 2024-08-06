from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.schemas.event import EventBaseSchema
from app.services.event import event_create, event_list, event_subscribe, get_my_events

security = HTTPBasic()

router = APIRouter(
    prefix="/events",
    tags=["🪩🫧🍸🥂🫧✧˖° Events"],
)


@router.post('', response_model=EventBaseSchema)
async def create(event: Annotated[EventBaseSchema, Depends()]):
    return await event_create(event)

@router.get('', response_model=list[EventBaseSchema])
async def get_list():
    return await event_list()

@router.post('/{event_id}', response_model=EventBaseSchema)
async def subscribe(event_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    return await event_subscribe(event_id, credentials)


@router.get('/my', response_model=list[EventBaseSchema])
async def get_my(credentials: HTTPBasicCredentials = Depends(security)):
    return await get_my_events(credentials)