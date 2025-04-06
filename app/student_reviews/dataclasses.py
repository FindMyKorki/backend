from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StudentReview(BaseModel):
    id: int
    created_at: datetime
    tutor_id: str
    student_id: str
    rating: float
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStudentReview(BaseModel):
    rating: float
    comment: Optional[str] = None

    class Config:
        from_attributes = True