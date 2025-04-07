from pydantic import BaseModel
from datetime import datetime


class Unavailability(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


class CreateUnavailabilityRequest(BaseModel):
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True
