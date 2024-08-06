from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from app.database.models import User
from app.schemas.user import UserSchema


class EventBaseSchema(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    meeting_time: datetime
    description: str = Field(min_length=2, max_length=255)
    # users: Optional[List[UserSchema]]

    model_config = ConfigDict(from_attributes=True)

