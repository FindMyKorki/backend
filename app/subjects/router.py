from fastapi import APIRouter
from subjects.dataclasses import Subject, CreateSubjectRequest
from subjects.service import SubjectsService

subjects_router = APIRouter()
subjects_service = SubjectsService()


@subjects_router.get("/subjects", response_model=list[Subject])
async def get_subjects():
    """
    Retrieve a list of all available subjects.

    Returns:
        list[Subject]: A list of all subjects available in the system.
    """
    return await subjects_service.get_subjects()


@subjects_router.post("/subjects", response_model=CreateSubjectRequest)
async def create_subject(create_subject_data: CreateSubjectRequest):
    """
    Create a new subject in the system.

    Args:
        create_subject_data (CreateSubjectRequest): The data needed to create a new subject (e.g., name, description).

    Returns:
        CreateSubjectRequest: The created subject.
    """
    return await subjects_service.create_subject(create_subject_data)
