from crud.crud_provider import CRUDProvider
from .dataclasses import Subject, UpsertSubject


crud_provider = CRUDProvider("subjects")


class SubjectService:
    async def create_subject(self, subject: UpsertSubject, id: int = None) -> Subject:
        new_subject = await crud_provider.create(subject.model_dump(), id)

        return Subject.model_validate(new_subject)

    async def get_subject(self, id: int) -> Subject:
        subject = await crud_provider.get(id)

        return Subject.model_validate(subject)

    async def get_all_subjects(self) -> list[Subject]:
        subjects = await crud_provider.get_all()

        return [Subject.model_validate(subject) for subject in subjects]

    async def update_subject(self, subject: UpsertSubject, id: int = None) -> Subject:
        updated_subject = await crud_provider.update(subject.model_dump(), id)

        return Subject.model_validate(updated_subject)

    async def delete_subject(self, id: int) -> Subject:
        deleted_subject = await crud_provider.delete(id)

        return Subject.model_validate(deleted_subject)

