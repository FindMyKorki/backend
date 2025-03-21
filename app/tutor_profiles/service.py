from tutor_profiles.dataclasses import TutorProfile, CreateTutorProfile, UpdateTutorProfile
from core.db_connection import supabase


class TutorProfilesService:
    async def get_tutor_profiles(self) -> list[TutorProfile]:
        tutor_profiles = (
            supabase.table("tutor_profiles")
            .select("*")
            .execute()
        )
        return tutor_profiles.data

    async def get_tutor_profile(self, profile_id: int) -> TutorProfile:
        tutor_profile = (
            supabase.table("tutor_profiles")
            .select("*")
            .eq("id", profile_id)
            .execute()
        )
        return tutor_profile.data[0] if tutor_profile.data else None

    async def get_tutor_profile_by_user(self, user_id: int) -> TutorProfile:
        tutor_profile = (
            supabase.table("tutor_profiles")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return tutor_profile.data[0] if tutor_profile.data else None

    async def create_tutor_profile(self, create_tutor_profile_data: CreateTutorProfile) -> str:
        new_tutor_profile = (
            supabase.table("tutor_profiles")
            .insert(create_tutor_profile_data.model_dump())
            .execute()
        )

        profile_id = new_tutor_profile.data[0].get("id")

        return f"Created new tutor profile with id {profile_id}"

    async def update_tutor_profile(self, profile_id: int, update_data: UpdateTutorProfile) -> str:
        # Filter out None values
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

        if not update_dict:
            return "No fields to update"

        updated_profile = (
            supabase.table("tutor_profiles")
            .update(update_dict)
            .eq("id", profile_id)
            .execute()
        )

        return f"Updated tutor profile with id {profile_id}"

    async def delete_tutor_profile(self, profile_id: int) -> str:
        deleted_profile = (
            supabase.table("tutor_profiles")
            .delete()
            .eq("id", profile_id)
            .execute()
        )

        return f"Deleted tutor profile with id {profile_id}"