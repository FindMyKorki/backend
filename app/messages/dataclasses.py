from pydantic import BaseModel


class UpsertSubject(BaseModel):
    sender_id: str
    content: dict
    is_read: bool | None = None
    chat_id: int | None = None
    is_media: bool | None = None

    class Config:
        from_attributes = True


class Message(UpsertSubject):
    id: int
    sent_at: str
