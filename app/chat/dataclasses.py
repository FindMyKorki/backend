from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

# input model, it is used when frontend sends new message with POST /send-message
class MessageCreate(BaseModel):
    sender_id: uuid.UUID
    chat_id: int
    content: Dict[str, Any] #json in form of a dict
    is_media: Optional[bool] = False

#'answer' model, it is used after writing message to supabase and returns it to frontend
class MessageResponse(BaseModel):
    id: uuid.UUID
    sender_id: uuid.UUID
    chat_id: uuid.UUID
    content: str
    sent_at: datetime
    is_read: bool
    is_media: bool