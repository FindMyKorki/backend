from core.db_connection import supabase
from .dataclasses import MessageResponse, ChatReportRequest, ChatResponse, Message
from fastapi import HTTPException


class ChatsService:
    async def get_tutor_chats(self, tutor_id: str) -> list[ChatResponse]:
        """Get all chats for tutor with last messages"""
        chats = supabase.rpc("get_tutor_chats_with_last_messages", {"p_tutor_id": tutor_id}).execute()

        if not chats.data: raise HTTPException(404, "No chats found")

        return chats.data


    async def get_student_chats(self, student_id: str):
        """Get all chats for student with last messages"""
        chats = supabase.rpc("get_student_chats_with_last_messages", {"p_student_id": student_id}).execute()

        if not chats.data: raise HTTPException(404, "No chats found")

        return chats.data


    async def get_chat_messages(self, chat_id: int, user_id: str) -> MessageResponse:
        """Get all messages for specific chat"""

        chat = supabase.table("chats").select("*").eq("id", chat_id).or_(f"student_id.eq.{user_id},tutor_id.eq.{user_id}").execute()

        if not chat.data: raise HTTPException(status_code=403, detail="You do not belong to this chat")

        messages = supabase.table("messages")\
                          .select("*")\
                          .eq("chat_id", chat_id)\
                          .order("sent_at")\
                          .execute()

        return MessageResponse(messages=messages.data or [])
      

    async def report_chat(self, chat_id: int, user_id: str, request: ChatReportRequest) -> str:
        """Report a chat conversation"""
        chat = supabase.table("chats") \
            .select("*") \
            .eq("id", chat_id) \
            .execute()

        if not chat.data:
            raise HTTPException(status_code=404, detail="Chat not found")

        chat_data = chat.data[0]
        reported_user_id = (
            chat_data["student_id"]
            if user_id == chat_data["tutor_id"]
            else chat_data["tutor_id"]
        )

        report_data = {
            "user_id": user_id,
            "reported_user_id": reported_user_id,
            "reason": request.reason,
            "message": f"Chat Report (ID: {chat_id}): {request.message}"
        }

        result = supabase.table("user_reports").insert(report_data).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create report")

        return "Chat successfully reported"
