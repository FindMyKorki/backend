from fastapi import APIRouter
from levels.dataclasses import Level, CreateLevelRequest
from levels.service import LevelsService

levels_router = APIRouter()
levels_service = LevelsService()


@levels_router.get("/levels", response_model=list[Level])
async def get_levels():
    """
    Retrieve a list of all available learning levels.

    Returns:
        list[Level]: A list of level objects, each containing id: int, and level: str.
    """
    return await levels_service.get_levels()


@levels_router.post("/levels", response_model=str)
async def create_level(create_level_data: CreateLevelRequest):
    """
    Create a new learning level that can be used to categorize tutors or students.

    Args:
        create_level_data (CreateLevelRequest): The data required to create a new level (level: str).

    Returns:
        str: A confirmation message indicating the level was successfully created.
    """
    return await levels_service.create_level(create_level_data)
