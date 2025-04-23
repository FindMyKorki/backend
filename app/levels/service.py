from core.db_connection import supabase
from levels.dataclasses import Level, CreateLevelRequest


class LevelsService:
    async def get_levels(self) -> list[Level]:
        levels = supabase.table("levels").select("*").execute()
        return levels.data

    async def create_level(self, create_level_data: CreateLevelRequest) -> str:
        supabase.table("levels").insert(create_level_data.model_dump()).execute()
        return 'Level created successfully'
