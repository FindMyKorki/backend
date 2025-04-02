from datetime import datetime, timezone, date
from pydantic import BaseModel, field_serializer
from typing import Optional
import calendar


class AvailableTimeBlock(BaseModel):
    """Model representing an available time block for a tutor"""
    start_date: datetime
    end_date: datetime

    @field_serializer('start_date', 'end_date')
    def serialize_datetime(self, dt: datetime) -> str:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()

    class Config:
        from_attributes = True


def get_end_of_current_month() -> datetime:
    """Returns the last day of the current month at 23:59:59"""
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return datetime(today.year, today.month, last_day, 23, 59, 59, tzinfo=timezone.utc)


class TutorAvailabilityRequest(BaseModel):
    """Model representing parameters for tutor availability query"""
    start_date: datetime = datetime.now(timezone.utc)
    end_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.end_date is None:
            self.end_date = get_end_of_current_month()
        
        if self.start_date.tzinfo is None:
            self.start_date = self.start_date.replace(tzinfo=timezone.utc)
        if self.end_date.tzinfo is None:
            self.end_date = self.end_date.replace(tzinfo=timezone.utc)


class TutorAvailabilityResponse(BaseModel):
    """Model representing response with available time blocks for a tutor"""
    available_blocks: list[AvailableTimeBlock]

    class Config:
        from_attributes = True 
