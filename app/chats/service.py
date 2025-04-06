from fastapi import HTTPException
from core.db_connection import supabase
from .dataclasses import Chat, Message, MessageResponse, ChatArchiveRequest, ChatReportRequest


class ChatsService:
    async def get_tutor_chats(self, tutor_id: str, current_user_id: str) -> list[Chat]:
        """Get all chats for a tutor"""
        # Validate that the current user is requesting their own chats
        if tutor_id != current_user_id:
            raise HTTPException(status_code=403, detail="You can only access your own chats")
            
        chats = (
            supabase.table("chats")
            .select("*")
            .eq("tutor_id", tutor_id)
            .execute()
        )
        
        if not chats.data:
            return []
            
        return chats.data
    
    async def get_student_chats(self, student_id: str, current_user_id: str) -> list[Chat]:
        """Get all chats for a student"""
        # Validate that the current user is requesting their own chats
        if student_id != current_user_id:
            raise HTTPException(status_code=403, detail="You can only access your own chats")
            
        chats = (
            supabase.table("chats")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )
        
        if not chats.data:
            return []
            
        return chats.data
    
    async def archive_chat(self, chat_id: int, request: ChatArchiveRequest, current_user_id: str) -> str:
        """Archive a chat"""
        chat = (
            supabase.table("chats")
            .select("*")
            .eq("id", chat_id)
            .execute()
        )
        
        if not chat.data or len(chat.data) == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
            
        # Validate that the current user is part of the chat
        chat_data = chat.data[0]
        if chat_data["tutor_id"] != current_user_id and chat_data["student_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="You can only archive your own chats")
        
        # Update the chat archived status
        supabase.table("chats").update(
            {"is_archived": request.is_archived}
        ).eq("id", chat_id).execute()
        
        return f"Chat {chat_id} has been {'archived' if request.is_archived else 'unarchived'}"
    
    async def report_chat(self, chat_id: int, current_user_id: str, request: ChatReportRequest) -> str:
        """Report a chat"""
        chat = (
            supabase.table("chats")
            .select("*")
            .eq("id", chat_id)
            .execute()
        )
        
        if not chat.data or len(chat.data) == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
            
        # Validate that the current user is part of the chat
        chat_data = chat.data[0]
        if chat_data["tutor_id"] != current_user_id and chat_data["student_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="You can only report chats you're part of")
        
        # Get the other participant of the chat to report
        reported_user_id = None
        
        if current_user_id == chat_data["tutor_id"]:
            reported_user_id = chat_data["student_id"]
        else:
            reported_user_id = chat_data["tutor_id"]
        
        # Create a user report
        report_data = {
            "user_id": current_user_id,
            "reported_user_id": reported_user_id,
            "reason": f"Chat report (Chat ID: {chat_id}): {request.reason}",
            "message": request.message
        }
        
        result = supabase.table("user_reports").insert(report_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create chat report")
        
        return f"Chat {chat_id} has been reported"
    
    async def get_chat_messages(self, chat_id: int, current_user_id: str) -> MessageResponse:
        """Get all messages for a chat"""
        chat = (
            supabase.table("chats")
            .select("*")
            .eq("id", chat_id)
            .execute()
        )
        
        if not chat.data or len(chat.data) == 0:
            raise HTTPException(status_code=404, detail="Chat not found")
            
        # Validate that the current user is part of the chat
        chat_data = chat.data[0]
        if chat_data["tutor_id"] != current_user_id and chat_data["student_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="You can only access messages from your own chats")
        
        messages = (
            supabase.table("messages")
            .select("*")
            .eq("chat_id", chat_id)
            .order("created_at", desc=False)
            .execute()
        )
        
        return MessageResponse(messages=messages.data or [])