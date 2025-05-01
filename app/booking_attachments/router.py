from typing import List, Annotated

from fastapi import APIRouter, Depends, Path, File, UploadFile, HTTPException, status, Form
from gotrue.types import UserResponse
from users.auth import authenticate_user
from fastapi.responses import JSONResponse
from .service import BookingAttachmentService

attachments_router = APIRouter()

# Example endpoint for uploading files, feel free to test it
@attachments_router.post("/{booking_id}/upload-attachment")
async def upload_files(files: Annotated[List[UploadFile], File()], booking_id: int = Path(...)):
    return await BookingAttachmentService.upload_files(booking_id, files)