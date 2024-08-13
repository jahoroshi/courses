from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from src.auth.schemas import UserSchema


class EventSubscriptionBaseSchema(BaseModel):
    """
    Base schema for event subscription data.
    Contains fields for configuring notifications and linking them to events.
    """

    # Time for the first notification, must be a datetime object
    first_notification: datetime

    # Optional time for the second notification, must be a datetime object
    second_notification: Optional[datetime] = None

    # ID of the event to which the subscription is linked
    event_id: int

    # Enable model configuration to load from attributes
    model_config = ConfigDict(from_attributes=True)


class EventSubscriptionShowSchema(EventSubscriptionBaseSchema):
    """
    Schema for displaying event subscription details.
    Inherits fields from EventSubscriptionBaseSchema and adds task IDs and user ID.
    """

    # Task ID for the first notification, must be a string with a maximum length of 50 characters
    first_task_id: str = Field(max_length=50)

    # Optional Task ID for the second notification, must be a string with a maximum length of 50 characters
    second_task_id: Optional[str] = Field(max_length=50)

    # ID of the user who subscribed to the event
    user_id: int


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

    notifications: Optional[List[EventSubscriptionShowSchema]]

    # Enable model configuration to load from attributes
    model_config = ConfigDict(from_attributes=True)
