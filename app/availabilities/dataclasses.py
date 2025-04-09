from datetime import datetime
from pydantic import BaseModel


class UnavailabilityHours(BaseModel):
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


class AvailabilityHours(UnavailabilityHours):
    recurrence_rule: str
