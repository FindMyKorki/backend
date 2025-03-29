from datetime import datetime
from pydantic import BaseModel, field_serializer


class AvailableTimeBlock(BaseModel):
    """Model representing an available time block for a tutor"""
    start_date: datetime
    end_date: datetime

    @field_serializer('start_date', 'end_date')
    def serialize_datetime(self, dt: datetime) -> str:
        if dt.tzinfo is None:
            from datetime import timezone
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()

    class Config:
        from_attributes = True


class TutorAvailabilityRequest(BaseModel):
    """Model representing parameters for tutor availability query"""
    tutor_id: str
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True


class TutorAvailabilityResponse(BaseModel):
    """Model representing response with available time blocks for a tutor"""
    available_blocks: list[AvailableTimeBlock]

    class Config:
        from_attributes = True 
