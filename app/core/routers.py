from fastapi import APIRouter
from typing import List

from test_lessons.router import test_lessons_router
from users.router import users_router
from profiles.router import profiles_router
from tutors_availability.router import tutors_availability_router
from tutors.router import tutors_router
from chats.router import chats_router
from student_reviews.router import student_reviews_router
from issue_reports.router import issue_reports_router
from user_reports.router import user_reports_router
from offer_reports.router import offer_reports_router


class Router:
    def __init__(self, router: APIRouter, tag: str):
        self.router = router
        self.tag = tag

# Add routers here
registered_routers: List[Router] = [
    Router(router=test_lessons_router, tag="Test Lessons"),
    Router(router=users_router, tag="Users"),
    Router(router=profiles_router, tag="Profiles"),
    Router(router=tutors_availability_router, tag="Tutors Availability"),
    Router(router=tutors_router, tag="Tutors"),
    Router(router=chats_router, tag="Chats"),
    Router(router=student_reviews_router, tag="Student Reviews"),
    Router(router=issue_reports_router, tag="Issue Reports"),
    Router(router=user_reports_router, tag="User Reports"),
    Router(router=offer_reports_router, tag="Offer Reports"),
]
