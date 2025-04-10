from fastapi import HTTPException
from core.db_connection import supabase
from .dataclasses import ChatWithLastMessage, MessageResponse, ChatReportRequest


class ChatsService:
    async def get_tutor_chats(self, tutor_id: str) -> list[ChatWithLastMessage]:
        """Get all chats for tutor with last messages"""
        chats = supabase.table("chats")\
                       .select("*")\
                       .eq("tutor_id", tutor_id)\
                       .execute()
        
        if not chats.data:
            return []
            
        return await self._enrich_chats_with_last_message(chats.data)
    
    async def get_student_chats(self, student_id: str) -> list[ChatWithLastMessage]:
        """Get all chats for student with last messages"""
        chats = supabase.table("chats")\
                       .select("*")\
                       .eq("student_id", student_id)\
                       .execute()
        
        if not chats.data:
            return []
            
        return await self._enrich_chats_with_last_message(chats.data)
    
    async def _enrich_chats_with_last_message(self, chats: list) -> list[ChatWithLastMessage]:
        """Add last message to each chat"""
        enriched_chats = []
        
        for chat in chats:
            last_message = supabase.table("messages")\
                                  .select("*")\
                                  .eq("chat_id", chat["id"])\
                                  .order("created_at", desc=True)\
                                  .limit(1)\
                                  .execute()
            
            enriched_chats.append({
                **chat,
                "last_message": last_message.data[0] if last_message.data else None
            })
            
        return enriched_chats
    
    async def get_chat_messages(self, chat_id: int) -> MessageResponse:
        """Get all messages for specific chat"""
        messages = supabase.table("messages")\
                          .select("*")\
                          .eq("chat_id", chat_id)\
                          .order("sent_at")\
                          .execute()
        
        return MessageResponse(messages=messages.data or [])
    
    async def report_chat(self, chat_id: int, user_id: str, request: ChatReportRequest) -> str:
        """Report a chat conversation"""
        chat = supabase.table("chats")\
                      .select("*")\
                      .eq("id", chat_id)\
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