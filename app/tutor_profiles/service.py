from .dataclasses import TutorProfile, UpsertTutorProfile
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('tutor_profiles')


class TutorProfilesService:
    async def create_tutor_profile(self, id: str, profile: UpsertTutorProfile) -> TutorProfile:
        new_tutor_profile = await crud_provider.create(profile.model_dump(), id)

        return TutorProfile.model_validate(new_tutor_profile)

    async def get_tutor_profile(self, id: str) -> TutorProfile:
        tutor_profile: dict = await crud_provider.get(id)

        return TutorProfile.model_validate(tutor_profile)

    async def update_tutor_profile(self, id: str, profile: UpsertTutorProfile) -> TutorProfile:
        updated_tutor_profile = await crud_provider.update(profile.model_dump(), id)

        return TutorProfile.model_validate(updated_tutor_profile)

    async def delete_tutor_profile(self, id: str) -> TutorProfile:
        deleted_tutor_profile = await crud_provider.delete(id)

        return TutorProfile.model_validate(deleted_tutor_profile)
