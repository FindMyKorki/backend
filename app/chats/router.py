from fastapi import APIRouter, Depends, Path
from gotrue.types import UserResponse
from users.auth import authenticate_user

from .dataclasses import ChatWithLastMessage, Message, ChatReportRequest
from .service import ChatsService

chats_router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)
chats_service = ChatsService()


@chats_router.get("/tutor", response_model=list[ChatWithLastMessage])
async def get_tutor_chats(_user_response: UserResponse = Depends(authenticate_user)):
    """
    Retrieve all chat conversations for a tutor, including the most recent message from each.

    Args:
        _user_response (UserResponse): The authenticated tutor's user data from the authentication dependency.

    Returns:
        list[ChatWithLastMessage]: A list of chat objects with the latest message in each conversation.
    """
    tutor_id = _user_response.user.id
    return await chats_service.get_tutor_chats(tutor_id)


@chats_router.get("/student", response_model=list[ChatWithLastMessage])
async def get_student_chats(_user_response: UserResponse = Depends(authenticate_user)):
    """
    Retrieve all chat conversations for a student, including the most recent message from each.

    Args:
        _user_response (UserResponse): The authenticated student's user data from the authentication dependency.

    Returns:
        list[ChatWithLastMessage]: A list of chat objects with the latest message in each conversation.
    """
    student_id = _user_response.user.id
    return await chats_service.get_student_chats(student_id)


@chats_router.get("/{chat_id}/messages", response_model=list[Message])
async def get_chat_messages(
        chat_id: int = Path(...),
        _user_response: UserResponse = Depends(authenticate_user)
):
    """
    Retrieve all messages from a specific chat conversation.

    Args:
        chat_id (int): The unique identifier of the chat.
        _user_response (UserResponse): The authenticated user accessing the chat.

    Returns:
        list[Message]: A list of message objects from the specified chat.
    """
    return await chats_service.get_chat_messages(chat_id)


@chats_router.post("/{chat_id}/report", response_model=str)
async def report_chat(
        request: ChatReportRequest,
        chat_id: int = Path(...),
        _user_response: UserResponse = Depends(authenticate_user)
):
    """
    Report a specific chat conversation for review or moderation.

    Args:
        request (ChatReportRequest): The reason and details for reporting the chat.
        chat_id (int): The unique identifier of the chat to be reported.
        _user_response (UserResponse): The authenticated user submitting the report.

    Returns:
        str: A confirmation message indicating the report was submitted.
    """
    return await chats_service.report_chat(
        chat_id,
        _user_response.user.id,
        request
    )
