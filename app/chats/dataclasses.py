from datetime import datetime
from pydantic import BaseModel
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



class Chat(BaseModel):
    id: int
    created_at: datetime
    last_updated_at: datetime
    tutor_id: str
    student_id: str

    class Config:
        from_attributes = True


class ChatWithLastMessage(Chat):
    last_message: Optional[Message] = None

    class Config:
        from_attributes = True


class ChatReportRequest(BaseModel):
    reason: str
    message: str

    class Config:
        from_attributes = True
