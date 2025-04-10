from pydantic import BaseModel
from datetime import datetime


class BaseUnavailability(BaseModel):
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


class Unavailability(BaseUnavailability):
    id: int