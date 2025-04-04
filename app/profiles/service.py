from .dataclasses import UpsertProfile, Profile
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('profiles')


class ProfilesService:
    async def create_profile(self, profile: UpsertProfile, user_id: str) -> Profile:
        new_profile = await crud_provider.create(profile.model_dump(), user_id)

        return Profile.model_validate(new_profile)

    async def get_profile(self, id: str) -> Profile:
        profile = await crud_provider.get(id)

        return Profile.model_validate(profile)

    async def update_profile(self, id: str, profile: UpsertProfile) -> Profile:
        updated_profile = await crud_provider.update(profile.model_dump(), id)

        return Profile.model_validate(updated_profile)

    async def delete_profile(self, id: str):
        deleted_profile = await crud_provider.delete(id)

        return Profile.model_validate(deleted_profile)
    