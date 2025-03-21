from tutor_profiles.service import TutorProfilesService
from tutor_profiles.dataclasses import TutorProfile, CreateTutorProfile, UpdateTutorProfile

from fastapi import APIRouter, HTTPException, Path, Query

tutor_profiles_router = APIRouter()
tutor_profiles_service = TutorProfilesService()


@tutor_profiles_router.get("/tutor-profiles", response_model=list[TutorProfile])
async def get_tutor_profiles():
    return await tutor_profiles_service.get_tutor_profiles()


@tutor_profiles_router.get("/tutor-profile/{profile_id}", response_model=TutorProfile)
async def get_tutor_profile(profile_id: int = Path(..., title="The ID of the tutor profile")):
    profile = await tutor_profiles_service.get_tutor_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Tutor profile not found")
    return profile


@tutor_profiles_router.get("/tutor-profile/user/{user_id}", response_model=TutorProfile)
async def get_tutor_profile_by_user(user_id: int = Path(..., title="The user ID")):
    profile = await tutor_profiles_service.get_tutor_profile_by_user(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Tutor profile not found for this user")
    return profile


@tutor_profiles_router.post("/tutor-profile", response_model=str)
async def create_tutor_profile(create_tutor_profile_data: CreateTutorProfile):
    return await tutor_profiles_service.create_tutor_profile(create_tutor_profile_data)


@tutor_profiles_router.put("/tutor-profile/{profile_id}", response_model=str)
async def update_tutor_profile(
        update_data: UpdateTutorProfile,
        profile_id: int = Path(..., title="The ID of the tutor profile to update")
):
    # Check if profile exists
    profile = await tutor_profiles_service.get_tutor_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Tutor profile not found")

    return await tutor_profiles_service.update_tutor_profile(profile_id, update_data)


@tutor_profiles_router.delete("/tutor-profile/{profile_id}", response_model=str)
async def delete_tutor_profile(profile_id: int = Path(..., title="The ID of the tutor profile to delete")):
    # Check if profile exists
    profile = await tutor_profiles_service.get_tutor_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Tutor profile not found")

    return await tutor_profiles_service.delete_tutor_profile(profile_id)