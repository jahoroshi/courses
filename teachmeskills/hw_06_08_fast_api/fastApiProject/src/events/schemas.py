from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from src.auth.schemas import UserSchema

class EventBaseSchema(BaseModel):
    """
    Base schema for event data.
    Contains common fields for events: name, meeting time, and description.
    """

    # Name of the event, must be a string between 2 and 255 characters
    name: str = Field(min_length=2, max_length=255)

    # Meeting time of the event, must be a datetime object
    meeting_time: datetime

    # Description of the event, must be a string between 2 and 255 characters
    description: str = Field(min_length=2, max_length=255)

class EventShowSchema(EventBaseSchema):
    """
    Schema for representing an event with additional fields.
    Inherits fields from EventBaseSchema and adds the id and users fields.
    """

    # ID of the event, type int
    id: int

    # List of users attending the event, optional
    users: Optional[List[UserSchema]]

    # Enable model configuration to load from attributes
    model_config = ConfigDict(from_attributes=True)
