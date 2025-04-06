from fastapi import APIRouter, Depends
from users.auth import authenticate_user, authenticate_profile
from .service import ChatsService
from .dataclasses import Chat, MessageResponse, ChatArchiveRequest, ChatReportRequest


chats_router = APIRouter()
chats_service = ChatsService()


@chats_router.get("/tutor-chats/{tutor_id}", response_model=list[Chat])
async def get_tutor_chats(tutor_id: str, user_response=Depends(authenticate_user)):
    """Get all chats for a tutor"""
    return await chats_service.get_tutor_chats(tutor_id, user_response.user.id)


@chats_router.get("/student-chats/{student_id}", response_model=list[Chat])
async def get_student_chats(student_id: str, user_response=Depends(authenticate_user)):
    """Get all chats for a student"""
    return await chats_service.get_student_chats(student_id, user_response.user.id)


@chats_router.post("/chats/{chat_id}:archive", response_model=str)
async def archive_chat(chat_id: int, request: ChatArchiveRequest, user_response=Depends(authenticate_user)):
    """Archive or unarchive a chat"""
    return await chats_service.archive_chat(chat_id, request, user_response.user.id)


@chats_router.post("/chats/{chat_id}:report", response_model=str)
async def report_chat(
    chat_id: int, 
    request: ChatReportRequest, 
    user_response=Depends(authenticate_user)
):
    """Report a chat"""
    return await chats_service.report_chat(chat_id, user_response.user.id, request)


@chats_router.get("/chats/{chat_id}/messages", response_model=MessageResponse)
async def get_chat_messages(chat_id: int, user_response=Depends(authenticate_user)):
    """Get all messages for a chat"""
    return await chats_service.get_chat_messages(chat_id, user_response.user.id)