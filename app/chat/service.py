import uuid
from datetime import datetime, timezone
from core.db_connection import supabase
from .dataclasses import MessageCreate, MessageResponse

TABLE_NAME = "messages"  

async def create_message(message: MessageCreate) -> MessageResponse:
    """Adds message to supabase and returns it as MessageResponse"""
    
    new_message = {
        "id": str(uuid.uuid4()),  #in table messages id is currently int but i think uuid would work better in this case
        "sender_id": str(message.sender_id),
        "chat_id": str(message.chat_id),
        "content": message.content,  
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "is_read": False,  # default value
        "is_media": message.is_media
    }
    
    response = supabase.table(TABLE_NAME).insert(new_message).execute()
    
    if response.error:
        raise Exception(f"Database insert error: {response.error}")
    
    return MessageResponse(**new_message)

async def get_chat_messages(chat_id: uuid.UUID):
    """Downloads all messages for given chat"""
    response = supabase.table(TABLE_NAME).select("*").eq("chat_id", str(chat_id)).execute()

    if response.error:
        raise Exception(f"Database fetch error: {response.error}")
    
    return [MessageResponse(**msg) for msg in response.data]

async def mark_as_read(message_id: uuid.UUID):
    """Mark message as is read"""
    response = (
        supabase.table(TABLE_NAME)
        .update({"is_read": True})
        .eq("id", str(message_id))
        .execute()
    )

    if response.error:
        raise Exception(f"Database update error: {response.error}")

    return {"message": "Message marked as read"}

def subscribe_to_messages(callback):
    """Function for real time chat"""
    supabase.realtime.on('postgres_changes', table=TABLE_NAME, event='INSERT', callback=callback)
    supabase.realtime.subscribe()
