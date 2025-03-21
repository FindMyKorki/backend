from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TutorProfile(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    bio: str
    expertise: str
    hourly_rate: float
    availability: str

    class Config:
        from_attributes = True


class CreateTutorProfile(BaseModel):
    user_id: int
    bio: str
    expertise: str
    hourly_rate: float
    availability: str

    class Config:
        from_attributes = True


class UpdateTutorProfile(BaseModel):
    bio: Optional[str] = None
    expertise: Optional[str] = None
    hourly_rate: Optional[float] = None
    availability: Optional[str] = None

    class Config:
        from_attributes = True