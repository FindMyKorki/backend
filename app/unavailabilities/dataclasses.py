from datetime import datetime
from pydantic import BaseModel


class BaseUnavailability(BaseModel):
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


class Unavailability(BaseUnavailability):
    id: int
