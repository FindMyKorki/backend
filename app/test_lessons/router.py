from app.test_lessons.service import TestLessonsService
from app.test_lessons.dataclasses import TestLesson, CreateTestLesson
from fastapi import APIRouter


test_lessons_router = APIRouter()
test_lessons_service = TestLessonsService()

@test_lessons_router.get("/test-lessons", response_model=list[TestLesson])
async def get_test_lessons():
    return await test_lessons_service.get_test_lessons()

@test_lessons_router.post("/test-lesson", response_model=str)
async def create_test_lesson(create_test_lesson_data: CreateTestLesson):
    return await test_lessons_service.create_test_lesson(create_test_lesson_data)