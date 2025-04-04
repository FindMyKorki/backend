from pydantic import BaseModel

class Subject(BaseModel):
    id: int
    name: str
    icon_url: str
    is_custom: bool = False

    class Config:
        from_attributes = True

class CreateSubjectRequest(BaseModel):
    name: str
    icon_url: str
    is_custom: bool = False

    class Config:
        from_attributes = True