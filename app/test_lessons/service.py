from test_lessons.dataclasses import TestLesson, CreateTestLesson
from core.db_connection import supabase


class TestLessonsService:
    async def get_test_lessons(self) -> list[TestLesson]:
        test_lessons = (
            supabase.table("test_lessons")
            .select("*")
            .execute()
        )
        return test_lessons.data
    
    async def create_test_lesson(self, create_test_lesson_data: CreateTestLesson) -> str:
        new_test_lesson = (
            supabase.table("test_lessons")
            .insert(create_test_lesson_data.model_dump())
            .execute()
        )

        id = new_test_lesson.data[0].get("id")

        return f"Created new test lesson with id {id}"
