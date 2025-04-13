from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StudentReview(BaseModel):
    id: int
    created_at: datetime
    tutor_id: str  # UUID stored as string
    student_id: str  # UUID stored as string
    rating: int  # Changed from float to int to match the database
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStudentReview(BaseModel):
    comment: Optional[str] = None

    class Config:
        from_attributes = True