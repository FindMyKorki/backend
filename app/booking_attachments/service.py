from typing import List

from crud.crud_provider import CRUDProvider

from .dataclasses import BookingAttachment, UpsertBookingAttachment
from fastapi import APIRouter, Depends, Path, File, UploadFile, HTTPException, status
from gotrue.types import UserResponse
from users.auth import authenticate_user
from fastapi.responses import JSONResponse
from core.db_connection import supabase
import uuid

crud_provider = CRUDProvider("booking_attachments")

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "application/pdf",
    "application/zip",
    "application/x-zip-compressed",
}
MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB

class BookingAttachmentService:
    async def create_booking_attachment(self, booking_attachment: UpsertBookingAttachment,
                                        id: int = None) -> BookingAttachment:
        new_booking_attachment = await crud_provider.create(booking_attachment.model_dump(exclude="created_at"), id)

        return BookingAttachment.model_validate(new_booking_attachment)

    async def get_booking_attachment(self, id: int) -> BookingAttachment:
        booking_attachment = await crud_provider.get(id)

        return BookingAttachment.model_validate(booking_attachment)

    async def update_booking_attachment(self, booking_attachment: UpsertBookingAttachment,
                                        id: int = None) -> BookingAttachment:
        updated_booking_attachment = await crud_provider.update(booking_attachment.model_dump(exclude="created_at"), id)

        return BookingAttachment.model_validate(updated_booking_attachment)

    async def delete_booking_attachment(self, id: int) -> BookingAttachment:
        deleted_booking_attachment = await crud_provider.delete(id)

        return BookingAttachment.model_validate(deleted_booking_attachment)

    async def upload_files(self, booking_id: int, files: List[UploadFile] = File(...)):
        for file in files:
            # Validate content type
            if file.content_type not in ALLOWED_CONTENT_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported file type: {file.content_type}"
                )

            # Read file content in chunks to avoid memory issues
            size = 0
            chunk_size = 1024 * 1024  # 1MB
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File {file.filename} exceeds size limit of 8 MB"
                    )

            # reset file for upload
            await file.seek(0)

        files_data = []

        for file in files:
            file_data = await file.read()
            filename = str(uuid.uuid4())
            path = f"{booking_id}/${filename}"  # TODO: provide unique pathname
            res = (supabase.storage
                   .from_("attachments")
                   .upload(file=file_data, path=path,
                           file_options={"upsert": "false",
                                         "content-type": file.content_type}))

            if not res.path:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload {file.filename}: {res['error']['message']}"
                )
            files_data.append(res)

        return files_data