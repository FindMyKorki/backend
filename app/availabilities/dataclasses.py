from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BaseAvailability(BaseModel):
    start_time: datetime
    end_time: datetime
    recurrence_rule: Optional[str]

    class Config:
        from_attributes = True


class Availability(BaseAvailability):
    id: int
