from core.db_connection import supabase
from fastapi import HTTPException
from .dataclasses import TutorProfile, UpdateTutorProfile
from .utils import get_tutor_profile_data


class TutorsService:
    async def update_tutor_profile(self, tutor_id: str, request: UpdateTutorProfile) -> TutorProfile:
        """Update tutor profile information"""
        # Check if tutor profile exists
        tutor_profile = await get_tutor_profile_data(tutor_id)
        
        if not tutor_profile:
            raise HTTPException(status_code=404, detail="Tutor profile not found")
        
        # Build update data dictionary with only provided fields
        update_data = {}
        if request.bio is not None:
            update_data["bio"] = request.bio
        if request.bio_long is not None:
            update_data["bio_long"] = request.bio_long
        if request.contact_email is not None:
            update_data["contact_email"] = request.contact_email
        if request.phone_number is not None:
            update_data["phone_number"] = request.phone_number
            
        # Only update if there's data to update
        if update_data:
            result = (
                supabase.table("tutor_profiles")
                .update(update_data)
                .eq("id", tutor_id)
                .execute()
            )
            
        # Return the updated profile
        updated_profile = await get_tutor_profile_data(tutor_id)
        return updated_profile