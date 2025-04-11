from .dataclasses import CreateProfile, Profile
from .utils import get_profile_data
from fastapi import HTTPException
from core.db_connection import supabase


class ProfilesService:
    async def create_profile(self, create_profile: CreateProfile, user_id: str) -> Profile:
        create_profile = create_profile.model_dump()
        create_profile['id'] = user_id
        
        profile = await get_profile_data(user_id)

        if profile:
            raise HTTPException(409, 'Profile already exists')

        new_profile = (
            supabase.table('profiles')
            .insert(create_profile)
            .execute()
        )

        return await get_profile_data(user_id)
    
    async def get_profile(self, id: str):
        profile = await get_profile_data(id)

        if not profile:
            raise HTTPException(404, 'Profile not found')

        return profile
    