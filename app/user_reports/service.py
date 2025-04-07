from .dataclasses import UserReport, CreateUserReportRequest, UpdateUserReportRequest
from crud.crud_provider import CRUDProvider
from profiles.service import crud_provider as profiles_crud_provider


crud_provider = CRUDProvider('user_reports', 'user_id')


class UserReportsService:
    async def create_user_report(self, user_id: str, user_report: CreateUserReportRequest) -> UserReport:
        user_report = user_report.model_dump()
        user_report['user_id'] = user_id

        new_user_report = await crud_provider.create(user_report)

        await self.__attach_profile(new_user_report)

        return UserReport.model_validate(new_user_report)

    async def get_user_report(self, id: int, user_id: str) -> UserReport:
        user_report: dict = await crud_provider.get(id, user_id)

        await self.__attach_profile(user_report)

        return UserReport.model_validate(user_report)

    async def update_user_report(self, user_id, user_report: UpdateUserReportRequest) -> UserReport:
        updated_user_report = await crud_provider.update(user_report.model_dump(), None, user_id)

        await self.__attach_profile(updated_user_report)

        return UserReport.model_validate(updated_user_report)

    async def delete_user_report(self, id: int, user_id: str) -> UserReport:
        deleted_user_report = await crud_provider.delete(id, user_id)

        await self.__attach_profile(deleted_user_report)

        return UserReport.model_validate(deleted_user_report)

    async def __attach_profile(self, user_report: dict) -> None:
        id = user_report.get('reported_user_id')
        level = await profiles_crud_provider.get(id)
        user_report['reported_user'] = level