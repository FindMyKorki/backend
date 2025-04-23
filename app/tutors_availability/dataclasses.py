import calendar
from datetime import datetime, timezone, date
from pydantic import BaseModel, field_serializer
from typing import Optional


class AvailableTimeBlock(BaseModel):
    start_date: datetime
    end_date: datetime

    @field_serializer('start_date', 'end_date')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.replace(tzinfo=timezone.utc).isoformat() if dt.tzinfo is None else dt.isoformat()

    class Config:
        from_attributes = True


def get_end_of_current_month() -> datetime:
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return datetime(today.year, today.month, last_day, 23, 59, 59, tzinfo=timezone.utc)


class TutorAvailabilityResponse(BaseModel):
    available_blocks: list[AvailableTimeBlock]
    message: Optional[str] = None

    class Config:
        from_attributes = True
