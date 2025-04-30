from crud.crud_provider import CRUDProvider

from .dataclasses import TutorProfile, BaseTutorProfile

crud_provider = CRUDProvider('tutor_profiles')


class TutorProfilesService:
    async def create_tutor_profile(self, id: str, profile: BaseTutorProfile) -> TutorProfile:
        """
        Create a tutor profile for a given user.

        Args:
            id (str): UUID of the user the profile is associated with.
            profile (BaseTutorProfile): The tutor profile details to be created.

        Returns:
            TutorProfile: The created tutor profile.
        """
        new_tutor_profile = await crud_provider.create(profile.model_dump(), id)

        return TutorProfile.model_validate(new_tutor_profile)

    async def get_tutor_profile(self, id: str) -> TutorProfile:
        """
        Retrieve a tutor profile by its ID.

        Args:
            id (str): UUID of the tutor profile to retrieve.

        Returns:
            TutorProfile: The requested tutor profile.
        """
        tutor_profile = await crud_provider.get(id)

        return TutorProfile.model_validate(tutor_profile)

    async def update_tutor_profile(self, id: str, profile: BaseTutorProfile) -> TutorProfile:
        """
        Update an existing tutor profile.

        Args:
            id (str): UUID of the tutor profile to update.
            profile (BaseTutorProfile): The updated tutor profile data.

        Returns:
            TutorProfile: The updated tutor profile.
        """
        updated_tutor_profile = await crud_provider.update(profile.model_dump(), id)

        return TutorProfile.model_validate(updated_tutor_profile)

    async def delete_tutor_profile(self, id: str) -> TutorProfile:
        """
        Delete a tutor profile by its ID.

        Args:
            id (str): UUID of the tutor profile to delete.

        Returns:
            TutorProfile: The deleted tutor profile.
        """
        deleted_tutor_profile = await crud_provider.delete(id)

        return TutorProfile.model_validate(deleted_tutor_profile)
