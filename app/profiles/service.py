import os
import uuid
from http.client import HTTPException
from typing import Optional, List, Annotated
from fastapi import HTTPException, UploadFile, File, Form
from pydantic import ValidationError

from crud.crud_provider import CRUDProvider
from .dataclasses import BaseProfile, Profile, CreateProfileRequest, UpdateProfileRequest
from core.db_connection import supabase
from users.service import UsersService
from users.dataclasses import UserResponse
from users.dataclasses import MyUserResponse

SUPABASE_URL = os.getenv("SUPABASE_URL")

crud_provider = CRUDProvider('profiles')
users_service = UsersService()

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
}
MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB


class ProfilesService:
    async def create_profile(self, user_response: UserResponse, create_profile_data: CreateProfileRequest, avatar: Optional[List[UploadFile]] = None ) -> Profile:
        """
        Create a new profile for a user.

        Args:
            user_response (UserResponse): Authenticated user's data.
            create_profile_data (CreateProfileRequest): The profile details (files excluded) to be created.
            avatar (List[UploadFile]): Optional image file to be set as user's avatar

        Returns:
            Profile: The created user profile.
        """

        user_data = await users_service.get_self(user_response=user_response)

        if user_data.profile: raise HTTPException(409, "Profile already exists!")


        if avatar and avatar[0].size != 0:
            file_data = await self.upload_avatar(user_response.user.id, avatar)
            avatar_url = f"{SUPABASE_URL}/storage/v1/object/public/{file_data.full_path}"
        else:
            avatar_url = user_data.provider_avatar_url

        profile_to_create = Profile(id = user_response.user.id, full_name = create_profile_data.full_name, is_tutor = create_profile_data.is_tutor, avatar_url = avatar_url)

        new_profile = await crud_provider.create(profile_to_create.model_dump())

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

    async def update_profile(self, user_response: UserResponse, update_profile_data: UpdateProfileRequest, avatar: Optional[List[UploadFile]] = None) -> Profile:
        """
        Create a new profile for a user.

        Args:
            user_response (UserResponse): Authenticated user's data.
            update_profile_data (UpdateProfileRequest): The profile details (files excluded) to be updated.
            avatar (List[UploadFile]): Optional image file to be set as user's new avatar

        Returns:
            Profile: The created user profile.
        """

        user_data = await users_service.get_self(user_response=user_response)

        if not user_data.profile: raise HTTPException(409, "Profile doesn't exist yet!")


        if avatar and avatar[0].size != 0:
            file_data = await self.upload_avatar(user_response.user.id, avatar)
            avatar_url = f"{SUPABASE_URL}/storage/v1/object/public/{file_data.full_path}"

            if user_data.profile.avatar_url and SUPABASE_URL in user_data.profile.avatar_url:
                await self.remove_avatar(user_data.profile.avatar_url)

        elif update_profile_data.remove_avatar:
            avatar_url = user_data.provider_avatar_url

            if user_data.profile.avatar_url and SUPABASE_URL in user_data.profile.avatar_url:
                await self.remove_avatar(user_data.profile.avatar_url)

        profile_to_update = Profile(id = user_data.id, full_name=update_profile_data.full_name,
                                    is_tutor=user_data.profile.is_tutor, avatar_url=avatar_url)

        updated_profile = await crud_provider.update(profile_to_update.model_dump(), user_data.id)

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

    # async def _check_profile_exists(self, user_id: str, expected_value: bool):
    #     try:
    #         await crud_provider.get(user_id)
    #         if expected_value: return True
    #     except HTTPException as e:
    #         if e.status_code == 502:
    #             if not expected_value: return True
    #             raise HTTPException(409, "Profile doesn't exist yet!")
    #     raise HTTPException(409, "Profile already exists!")

    async def upload_avatar(self, user_id: str, files: List[UploadFile] = File(...)):
        avatar = files[0]
        if avatar.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {avatar.content_type}"
            )

        size = 0
        chunk_size = 1024 * 1024
        while True:
            chunk = await avatar.read(chunk_size)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"File {avatar.filename} exceeds size limit of 8 MB"
                )

        await avatar.seek(0)

        file_data = await avatar.read()
        filename =  str(uuid.uuid4())
        path = f"{user_id}/{filename}"
        res = (supabase.storage
               .from_("avatars")
               .upload(file=file_data, path=path,
                       file_options={"upsert": "false",
                                     "content-type": avatar.content_type}))

        if not res.path:
            raise HTTPException(
                status_code = 500,
                detail = f"Failed to upload {avatar.filename}"
            )

        return res

    async def remove_avatar(self, path: str):
        filepath = path.split(
            f"{SUPABASE_URL}/storage/v1/object/public/avatars/")[1]
        _ = supabase.storage.from_("avatars").remove([filepath])

async def _parse_from_create_request(is_tutor: Annotated[bool, Form()], full_name: Annotated[str, Form()]) -> CreateProfileRequest:
    try:
        return CreateProfileRequest(is_tutor=is_tutor, full_name=full_name)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

async def _parse_from_update_request(remove_avatar: Annotated[bool, Form()], full_name: Annotated[str, Form()]) -> UpdateProfileRequest:
    try:
        return UpdateProfileRequest(remove_avatar=remove_avatar, full_name=full_name)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

