from core.db_connection import supabase
from fastapi import HTTPException
from supabase import AuthApiError

from .dataclasses import Profile


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

    if profile.data and len(profile.data) > 0:
        return profile.data[0]

    return None
