from datetime import datetime, timezone
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


class TutorAvailabilityResponse(BaseModel):
    available_blocks: list[AvailableTimeBlock]
    message: Optional[str] = None

    class Config:
        from_attributes = True
