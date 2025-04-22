from availabilities.router import availabilities_router
from bookings.router import bookings_router
from chats.router import chats_router
from fastapi import APIRouter
from issue_reports.router import issue_reports_router
from levels.router import levels_router
from offer_reports.router import offer_reports_router
from profiles.router import profiles_router
from offers.router import offers_router
from profiles.router import profiles_router
from student_reviews.router import student_reviews_router
from subjects.router import subjects_router
from test_lessons.router import test_lessons_router
from reviews.router import reviews_router
from test_lessons.router import test_lessons_router
from tutors_availability.router import tutors_availability_router
from tutors.router import tutors_router
from typing import List
from user_reports.router import user_reports_router
from users.router import users_router
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
    Router(router=tutors_availability_router, tag="Tutors Availability"),
    Router(router=tutors_router, tag="Tutors"),
    Router(router=chats_router, tag="Chats"),
    Router(router=student_reviews_router, tag="Student Reviews"),
    Router(router=issue_reports_router, tag="Issue Reports"),
    Router(router=user_reports_router, tag="User Reports"),
    Router(router=offer_reports_router, tag="Offer Reports"),
    Router(router=subjects_router, tag="Subjects"),
    Router(router=levels_router, tag="Levels"),
    Router(router=bookings_router, tag="Bookings"),
    Router(router=offers_router, tag="Offers"),
    Router(router=reviews_router, tag="Reviews"),
    Router(router=availabilities_router, tag="(Un)availabilities"),
    Router(router=chat_logic_router, tag="Chat_realtime"),
    Router(router=chat_logic_router, tag="Chat Logic"),
]
