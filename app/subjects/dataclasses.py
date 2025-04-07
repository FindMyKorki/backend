from pydantic import BaseModel


class UpsertSubject(BaseModel):
    name: str
    icon_url: str | None = None
    is_custom: bool = True


    class Config:
        from_attributes = True


class Subject(UpsertSubject):
    id: int


