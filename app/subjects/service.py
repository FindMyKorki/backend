from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from fastapi import HTTPException
from subjects.dataclasses import Subject, CreateSubjectRequest

from .dataclasses import Subject, UpsertSubject

crud_provider = CRUDProvider("subjects")


class SubjectsService:
    async def get_subjects(self) -> list[Subject]:
        subjects = supabase.table("subjects").select("*").execute()
        return subjects.data

    async def create_subject(self, create_subject_data: CreateSubjectRequest) -> str:
        supabase.table("subjects").insert(create_subject_data.model_dump()).execute()
        return 'Subject created successfully'

    # CRUD
    async def create_subject2(self, subject: UpsertSubject, id: int = None) -> Subject:
        new_subject = await crud_provider.create(subject.model_dump(), id)

        return Subject.model_validate(new_subject)

    async def get_subject(self, id: int) -> Subject:
        subject = await crud_provider.get(id)

        return Subject.model_validate(subject)

    async def update_subject(self, subject: UpsertSubject | Subject, id: int = None) -> Subject:
        updated_subject = await crud_provider.update(subject.model_dump(), id)

        return Subject.model_validate(updated_subject)

    async def delete_subject(self, id: int) -> Subject:
        deleted_subject = await crud_provider.delete(id)

        return Subject.model_validate(deleted_subject)
