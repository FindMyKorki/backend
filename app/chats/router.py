from fastapi import APIRouter, Depends
from users.auth import authenticate_user
from .service import ChatsService
from .dataclasses import MessageResponse, ChatReportRequest, ChatResponse


chats_router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)
chats_service = ChatsService()


@chats_router.get("/tutor", response_model=list[ChatResponse])
async def get_tutor_chats(user_response=Depends(authenticate_user)):
    """Get all chats for tutor with last messages"""
    tutor_id = user_response.user.id
    return await chats_service.get_tutor_chats(tutor_id)


@chats_router.get("/student", response_model=list[ChatResponse])
async def get_student_chats(user_response=Depends(authenticate_user)):
    """Get all chats for student with last messages"""
    student_id = user_response.user.id
    return await chats_service.get_student_chats(student_id)


@chats_router.get("/{chat_id}/messages", response_model=MessageResponse)
async def get_chat_messages(
    chat_id: int, 
    user_response=Depends(authenticate_user)
):
    """Get all messages for specific chat"""
    return await chats_service.get_chat_messages(chat_id, user_response.user.id)


@chats_router.post("/{chat_id}/report", response_model=str)
async def report_chat(
    chat_id: int,
    request: ChatReportRequest,
    user_response=Depends(authenticate_user)
):
    """Report a chat conversation"""
    return await chats_service.report_chat(
        chat_id, 
        user_response.user.id, 
        request
    )