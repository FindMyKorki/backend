from typing import Optional, Dict, Any

from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any


class TutorProfile(BaseModel):
    id: str  # uuid
    user_id: str  # uuid
    full_name: str
    bio: str
    price_per_hour: float
    availability: Dict[str, Any]
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True


class CreateTutorProfile(BaseModel):
    user_id: str  # uuid
    full_name: str
    bio: str
    price_per_hour: float
    availability: Dict[str, Any]

    class Config:
        from_attributes = True



class UpdateTutorProfile(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    price_per_hour: Optional[float] = None
    availability: Optional[Dict[str, Any]] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True