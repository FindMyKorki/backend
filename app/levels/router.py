from fastapi import APIRouter
from levels.dataclasses import Level, CreateLevelRequest
from levels.service import LevelsService

levels_router = APIRouter()
levels_service = LevelsService()


@levels_router.get("/levels", response_model=list[Level])
async def get_levels():
    return await levels_service.get_levels()


@levels_router.post("/levels", response_model=str)
async def create_level(create_level_data: CreateLevelRequest):
    return await levels_service.create_level(create_level_data)
