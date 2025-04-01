from .dataclasses import UserReport, CreateUserReportRequest, UpdateUserReportRequest
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('user_reports', 'user_id')


class UserReportsService:
    async def create_user_report(self, user_id: str, user_report: CreateUserReportRequest) -> UserReport:
        user_report = user_report.model_dump(exclude='id')
        user_report['user_id'] = user_id

        new_user_report = await crud_provider.create(user_report)

        return UserReport.model_validate(new_user_report)

    async def get_user_report(self, id: int, user_id: str) -> UserReport:
        user_report: dict = await crud_provider.get(id, user_id)

        return UserReport.model_validate(user_report)

    async def update_user_report(self, user_id, user_report: UpdateUserReportRequest) -> UserReport:
        updated_user_report = await crud_provider.update(user_report.id, user_report.model_dump(exclude='id'), user_id)

        return UserReport.model_validate(updated_user_report)

    async def delete_user_report(self, id: int, user_id: str) -> UserReport:
        deleted_user_report = await crud_provider.delete(id, user_id)

        return UserReport.model_validate(deleted_user_report)
