from .dataclasses import Profile
from core.db_connection import supabase
from supabase import AuthApiError
from fastapi import HTTPException

async def get_profile_data(id: str) -> Profile:
    try:
        user = supabase.auth.admin.get_user_by_id(id).user
    except AuthApiError:
        raise HTTPException(404, 'User not found')

    profile = (
        supabase.table('profiles')
        .select('*')
        .eq('id', id)
        .execute()
    )

    if profile.data:
        p_d = profile.data[0]
        profile = Profile(
            id=p_d.get('id'),
            full_name=p_d.get('full_name'),
            is_tutor=p_d.get('is_tutor'),
            created_at=p_d.get('created_at'),
            email=user.user_metadata.get('email'), 
            avatar_url=user.user_metadata.get('avatar_url')
        )
        return profile
    
    return None