from pydantic import BaseModel


class UpsertReview(BaseModel):
    student_id: str
    tutor_id: str
    rating: int | None = None
    comment: str

    class Config:
        from_attributes = True


class Review(UpsertReview):
    id: int
    created_at: str

