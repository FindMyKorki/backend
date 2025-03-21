from fastapi import APIRouter
from typing import List

from test_lessons.router import test_lessons_router
from users.router import users_router


class Router:
    def __init__(self, router: APIRouter, tag: str):
        self.router = router
        self.tag = tag

# Add routers here
registered_routers: List[Router] = [
    Router(router=test_lessons_router, tag="Test Lessons"),
    Router(router=users_router, tag="Users"),
]
