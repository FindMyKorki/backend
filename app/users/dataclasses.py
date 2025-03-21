from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    uid: int
    display_name: str
    email: str
    phone: str
    providers: str
    provider_type: str
    created_at: datetime
    last_sign_in_at: datetime

    class Config:
        from_attributes = True
