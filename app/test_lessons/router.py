from test_lessons.service import TestLessonsService
from test_lessons.dataclasses import TestLesson, CreateTestLesson
from users.auth import authenticate_user
from fastapi import APIRouter, Depends


test_lessons_router = APIRouter()
test_lessons_service = TestLessonsService()

@test_lessons_router.get("/test-lessons", response_model=list[TestLesson])
async def get_test_lessons(user_response=Depends(authenticate_user)):
    return await test_lessons_service.get_test_lessons()

@test_lessons_router.post("/test-lesson", response_model=str)
async def create_test_lesson(create_test_lesson_data: CreateTestLesson, user_response=Depends(authenticate_user)):
    return await test_lessons_service.create_test_lesson(create_test_lesson_data)