from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Availability(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    recurrence_rule: Optional[str]

    class Config:
        from_attributes = True


class CreateAvailabilityRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    recurrence_rule: Optional[str]

    class Config:
        from_attributes = True
