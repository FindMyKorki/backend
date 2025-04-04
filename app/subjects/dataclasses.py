from pydantic import BaseModel


class UpsertSubject(BaseModel):
    subject_name: str
    is_custom: bool
    icon_url: str | None = None

    class Config:
        from_attributes = True


class Subject(UpsertSubject):
    id: int


