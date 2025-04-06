from fastapi import HTTPException
from core.db_connection import supabase
from .dataclasses import Chat, Message, MessageResponse, ChatArchiveRequest, ChatReportRequest


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
    
    async def archive_chat(self, chat_id: int, request: ChatArchiveRequest) -> str:
        """Archive a chat"""
        chat = (
            supabase.table("chats")
            .select("*")
            .eq("id", chat_id)
            .execute()
        )
        
        if not chat.data or len(chat.data) == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Update the chat archived status
        supabase.table("chats").update(
            {"is_archived": request.is_archived}
        ).eq("id", chat_id).execute()
        
        return f"Chat {chat_id} has been {'archived' if request.is_archived else 'unarchived'}"
    
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
        
        # Create a user report for this chat
        report_data = {
            "user_id": user_id,
            "reported_chat_id": chat_id,
            "reason": request.reason,
            "message": request.message
        }
        
        supabase.table("user_reports").insert(report_data).execute()
        
        return f"Chat {chat_id} has been reported"
    
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