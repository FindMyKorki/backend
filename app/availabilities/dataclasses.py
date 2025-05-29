from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UnavailabilityHours(BaseModel):
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


class AvailabilityHours(UnavailabilityHours):
    recurrence_rule: Optional[str] = None

class UnavailabilityResponse(UnavailabilityHours):
    id: int
    tutor_id: str

class AvailabilityResponse(AvailabilityHours):
    id: int
    tutor_id: str