from core.db_connection import supabase
from fastapi import HTTPException
from .dataclasses import StudentReview, CreateStudentReview


class StudentReviewsService:
    async def get_student_reviews(self, student_id: str) -> list[StudentReview]:
        """Get all reviews for a student"""
        # Verify the student exists
        try:
            student = supabase.auth.admin.get_user_by_id(student_id).user
        except:
            raise HTTPException(status_code=404, detail="Student not found")
        
        reviews = (
            supabase.table("reviews")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )
        
        return reviews.data or []