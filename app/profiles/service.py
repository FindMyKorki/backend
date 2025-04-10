from .dataclasses import BaseProfile, Profile
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('profiles')


class ProfilesService:
    async def create_profile(self, user_id: str, profile: BaseProfile) -> Profile:
        """
        Create a new profile for a user.

        Args:
            user_id (str): UUID of the user associated with the profile.
            profile (BaseProfile): The profile details to be created.

        Returns:
            Profile: The created user profile.
        """
        new_profile = await crud_provider.create(profile.model_dump(), user_id)

        return Profile.model_validate(new_profile)

    async def get_profile(self, id: str) -> Profile:
        """
        Retrieve a user profile by its ID.

        Args:
            id (str): UUID of the profile to retrieve.

        Returns:
            Profile: The requested user profile.
        """
        profile = await crud_provider.get(id)

        return Profile.model_validate(profile)

    async def update_profile(self, id: str, profile: BaseProfile) -> Profile:
        """
        Update an existing user profile.

        Args:
            id (str): UUID of the profile to update.
            profile (BaseProfile): The updated profile data.

        Returns:
            Profile: The updated user profile.
        """
        updated_profile = await crud_provider.update(profile.model_dump(), id)

        return Profile.model_validate(updated_profile)

    async def delete_profile(self, id: str) -> Profile:
        """
        Delete a user profile by its ID.

        Args:
            id (str): UUID of the profile to delete.

        Returns:
            Profile: The deleted user profile.
        """
        deleted_profile = await crud_provider.delete(id)

        return Profile.model_validate(deleted_profile)
    