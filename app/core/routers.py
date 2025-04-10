from fastapi import APIRouter
from typing import List

from test_lessons.router import test_lessons_router
from users.router import users_router
from profiles.router import profiles_router
from chat_logic.router import chat_logic_router


class Router:
    def __init__(self, router: APIRouter, tag: str):
        self.router = router
        self.tag = tag

# Add routers here
registered_routers: List[Router] = [
    Router(router=test_lessons_router, tag="Test Lessons"),
    Router(router=users_router, tag="Users"),
    Router(router=profiles_router, tag="Profiles"),
    Router(router=chat_logic_router, tag="Chat_realtime"),
]
