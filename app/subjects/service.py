from fastapi import HTTPException
from subjects.dataclasses import Subject, CreateSubjectRequest
from core.db_connection import supabase

class SubjectsService:
    async def get_subjects(self) -> list[Subject]:
        subjects = supabase.table("subjects").select("*").execute()
        return HTTPException(200, subjects.data)
    
    async def create_subject(self, create_subject_data: CreateSubjectRequest) -> str:
        supabase.table("subjects").insert(create_subject_data.model_dump()).execute()
        return HTTPException(201,'Subject created successfully')