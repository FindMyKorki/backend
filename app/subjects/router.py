from subjects.service import SubjectsService
from subjects.dataclasses import Subject, CreateSubjectRequest

from fastapi import APIRouter

subjects_router = APIRouter()
subjects_service = SubjectsService()

@subjects_router.get("/subjects", response_model=list[Subject])
async def get_subjects():
    return await subjects_service.get_subjects()


@subjects_router.post("/subjects", response_model=str)
async def create_subject(create_subject_data: CreateSubjectRequest):
    return await subjects_service.create_subject(create_subject_data)