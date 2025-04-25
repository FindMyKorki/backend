from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import StudentReview


class StudentReviewsService:
    async def get_student_reviews(self, student_id: str) -> list[StudentReview]:
        """Get all reviews for a student"""
        await self._check_student_exists(student_id)

        # Using the correct table name "reviews" from your schema
        reviews = (
            supabase.table("reviews")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )

        return reviews.data or []

    async def _check_student_exists(self, student_id: str):
        crud_provider_tutor_profile = CRUDProvider('profiles', 'id')
        try:
            student = await crud_provider_tutor_profile.get(student_id)
            if student.get("is_tutor"):
                raise HTTPException(status_code=403, detail="You are not a student, but tutor!")
        except HTTPException as e:
            if e.status_code == 502:
                raise HTTPException(403, f"There is no student with this id!")
            raise
