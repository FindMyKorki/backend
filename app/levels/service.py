from fastapi import HTTPException
from levels.dataclasses import Level, CreateLevelRequest
from core.db_connection import supabase

class LevelsService:
    async def get_levels(self) -> list[Level]:
        levels = supabase.table("levels").select("*").execute()
        return HTTPException(200, levels.data)
    
    async def create_level(self, create_level_data: CreateLevelRequest) -> str:
        supabase.table("levels").insert(create_level_data.model_dump()).execute()
        return HTTPException(201, 'Level created successfully')