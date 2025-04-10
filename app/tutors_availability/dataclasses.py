from datetime import datetime, timezone, date
from pydantic import BaseModel, field_serializer
from typing import Optional
import calendar


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


class TutorAvailabilityRequest(BaseModel):
    start_date: datetime = datetime.now(timezone.utc)
    end_date: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.end_date = self.end_date or get_end_of_current_month()
        self.start_date = self.start_date.replace(tzinfo=timezone.utc) if self.start_date.tzinfo is None else self.start_date
        self.end_date = self.end_date.replace(tzinfo=timezone.utc) if self.end_date.tzinfo is None else self.end_date

    class Config:
        from_attributes = True


class TutorAvailabilityResponse(BaseModel):
    available_blocks: list[AvailableTimeBlock]
    message: Optional[str] = None

    class Config:
        from_attributes = True