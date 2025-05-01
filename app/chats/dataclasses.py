from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any


class Message(BaseModel):
    id: int
    sent_at: datetime  # Changed from created_at to sent_at to match DB
    chat_id: int
    sender_id: str
    content: Any  # Changed from str to Any since it's JSON in the database
    is_read: bool
    is_media: bool  # Changed from is_message to is_media to match DB

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    messages: List[Message]
    
    class Config:
        from_attributes = True


class Chat(BaseModel):
    id: int
    created_at: datetime
    last_updated_at: datetime
    tutor_id: str
    student_id: str

    class Config:
        from_attributes = True



class ChatReportRequest(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    chat_id: int
    their_id: str
    their_full_name: str
    their_avatar_url: Optional[str] = None
    last_message_id: Optional[int] = None
    last_message_sender_id: Optional[str] = None
    last_message_content: Optional[Any] = None
    last_message_is_media: Optional[bool] = None
    last_message_is_read: Optional[bool] = None
    last_message_sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True