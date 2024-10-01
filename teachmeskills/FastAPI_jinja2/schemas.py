# schemas.py
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

class ForkliftBase(BaseModel):
    brand: str
    number: str
    capacity: float

class ForkliftCreate(ForkliftBase):
    pass

class Forklift(ForkliftBase):
    id: int

    class Config:
        orm_mode = True

class DowntimeBase(BaseModel):
    end_time: Optional[datetime] = None
    reason: Optional[str] = None

class DowntimeCreate(DowntimeBase):
    forklift_id: int
    start_time: datetime

class Downtime(DowntimeBase):
    id: int
    forklift_id: int
    start_time: datetime
    downtime_duration: Optional[str] = None

    class Config:
        orm_mode = True

