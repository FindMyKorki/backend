from core.db_connection import supabase
from fastapi import HTTPException
from .dataclasses import StudentReview


class StudentReviewsService:
    async def get_student_reviews(self, student_id: str) -> list[StudentReview]:
        """Get all reviews for a student"""
        # Using the correct table name "reviews" from your schema
        reviews = (
            supabase.table("reviews")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )
        
        return reviews.data or []