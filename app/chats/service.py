from fastapi import HTTPException
from core.db_connection import supabase
from .dataclasses import Chat, Message, MessageResponse, ChatReportRequest


class ChatsService:
    async def get_tutor_chats(self, tutor_id: str) -> list[Chat]:
        """Get all chats for a tutor"""
        chats = (
            supabase.table("chats")
            .select("*")
            .eq("tutor_id", tutor_id)
            .execute()
        )
        
        if not chats.data:
            return []
            
        return chats.data
    
    async def get_student_chats(self, student_id: str) -> list[Chat]:
        """Get all chats for a student"""
        chats = (
            supabase.table("chats")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )
        
        if not chats.data:
            return []
            
        return chats.data
    
    async def report_chat(self, chat_id: int, user_id: str, request: ChatReportRequest) -> str:
        """Report a chat"""
        chat = (
            supabase.table("chats")
            .select("*")
            .eq("id", chat_id)
            .execute()
        )
        
        if not chat.data or len(chat.data) == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Since we can't directly report a chat (only users), we'll report the other participant
        # Get the chat data to determine who to report
        chat_data = chat.data[0]
        
        # Determine which user to report (the one that's not the reporter)
        reported_user_id = chat_data["student_id"] if user_id == chat_data["tutor_id"] else chat_data["tutor_id"]
        
        # Create a user report
        report_data = {
            "user_id": user_id,
            "reported_user_id": reported_user_id,
            "reason": request.reason,
            "message": request.message
        }
        
        result = supabase.table("user_reports").insert(report_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create report")
        
        return f"Chat {chat_id} participant has been reported"
    
    async def get_chat_messages(self, chat_id: int) -> MessageResponse:
        """Get all messages for a chat"""
        chat = (
            supabase.table("chats")
            .select("*")
            .eq("id", chat_id)
            .execute()
        )
        
        if not chat.data or len(chat.data) == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        messages = (
            supabase.table("messages")
            .select("*")
            .eq("chat_id", chat_id)
            .order("created_at", desc=False)
            .execute()
        )
        
        return MessageResponse(messages=messages.data or [])