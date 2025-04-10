from pydantic import BaseModel
from datetime import datetime
from typing import Any


class Message(BaseModel):
    id: int
    sender_id: str  # UUID in string format
    content: Any  # JSON
    sent_at: datetime
    is_read: bool
    chat_id: int
    is_media: bool

    class Config:
        from_attributes = True