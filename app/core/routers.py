from fastapi import APIRouter
from typing import List

from test_lessons.router import test_lessons_router
from tutor_profiles.router import tutor_profiles_router
from offers.router import offers_router
from bookings.router import bookings_router
from reviews.router import reviews_router


class Router:
    def __init__(self, router: APIRouter, tag: str):
        self.router = router
        self.tag = tag

# Add routers here
registered_routers: List[Router] = [
    Router(router=test_lessons_router, tag="Test Lessons"),
    Router(router=tutor_profiles_router, tag="Tutor Profiles"),
    Router(router=offers_router, tag="Offers"),
    Router(router=bookings_router, tag="Bookings"),
    Router(router=reviews_router, tag="Reviews"),
]