from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class Message(BaseModel):
    id: int
    created_at: datetime
    chat_id: int
    sender_id: str
    content: str
    is_read: bool

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