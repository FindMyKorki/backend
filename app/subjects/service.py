from subjects.dataclasses import Subject, CreateSubjectRequest
from core.db_connection import supabase

class SubjectsService:
    async def get_subjects(self) -> list[Subject]:
        try:
            subjects = supabase.table("subjects").select("*").execute()
        except Exception as e:
            raise Exception(f"Error fetching subjects: {str(e)}")
        
        return subjects.data
    
    async def create_subject(self, create_subject_data: CreateSubjectRequest) -> str:
        try:
            supabase.table("subjects").insert(create_subject_data.model_dump()).execute()
        except Exception as e:
            raise Exception(f"Error creating subject: {str(e)}")

        return 'Subject created successfully'