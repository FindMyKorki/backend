from core.db_connection import supabase
from .dataclasses import Message


class ChatLogicService:
    async def save_message(self, message_data: dict) -> Message:
        """Save a new message to the database"""
        result = supabase.table("messages").insert(message_data).execute()
        if not result.data:
            raise Exception("Failed to save message")
        return Message(**result.data[0])

    async def mark_as_read(self, chat_id: int, user_id: str):
        """Mark all messages in a chat as read by a specific user"""
        supabase.table("messages")\
                .update({"is_read": True})\
                .eq("chat_id", chat_id)\
                .eq("sender_id", user_id)\
                .execute()

    async def get_unread_messages(self, chat_id: int, user_id: str):
        """Get all unread messages for a chat"""
        messages = supabase.table("messages")\
                           .select("*")\
                           .eq("chat_id", chat_id)\
                           .eq("is_read", False)\
                           .execute()
        return [Message(**msg) for msg in messages.data]