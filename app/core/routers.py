from availabilities.router import availabilities_router
from fastapi import APIRouter
from offers.router import offers_router
from profiles.router import profiles_router
from subjects.router import subjects_router
from levels.router import levels_router
from bookings.router import bookings_router
from reviews.router import reviews_router
from test_lessons.router import test_lessons_router
from tutors.router import tutor_router
from typing import List
from users.router import users_router


class Router:
    def __init__(self, router: APIRouter, tag: str):
        self.router = router
        self.tag = tag


# Add routers here
registered_routers: List[Router] = [
    Router(router=test_lessons_router, tag="Test Lessons"),
    Router(router=users_router, tag="Users"),
    Router(router=profiles_router, tag="Profiles"),
    Router(router=subjects_router, tag="Subjects"),
    Router(router=levels_router, tag="Levels"),
    Router(router=bookings_router, tag="Bookings"),
    Router(router=tutor_router, tag="Tutors"),
    Router(router=offers_router, tag="Offers"),
    Router(router=reviews_router, tag="Reviews"),
    Router(router=availabilities_router, tag="(Un)availabilities"),
]
