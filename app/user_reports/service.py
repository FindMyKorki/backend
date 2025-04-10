from .dataclasses import UserReport, CreateUserReport, UpdateUserReport
from crud.crud_provider import CRUDProvider
from profiles.service import crud_provider as profiles_crud_provider


crud_provider = CRUDProvider('user_reports', 'user_id')


class UserReportsService:

    async def create_user_report(self, user_id: str, user_report: CreateUserReport) -> UserReport:
        """
        Create a new user report for a specific user.

        Args:
            user_id (str): UUID of the user submitting the report.
            user_report (CreateUserReportRequest): The report details to be created.

        Returns:
            UserReport: The created user report with attached profile information.
        """
        user_report = user_report.model_dump()
        user_report['user_id'] = user_id

        new_user_report = await crud_provider.create(user_report)

        await self.__attach_profile(new_user_report)

        return UserReport.model_validate(new_user_report)

    async def get_user_report(self, id: int, user_id: str) -> UserReport:
        """
        Retrieve a specific user report by its ID for a given user.

        Args:
            id (int): ID of the user report to retrieve.
            user_id (str): UUID of the user who owns the report.

        Returns:
            UserReport: The requested user report with attached profile information.
        """
        user_report = await crud_provider.get(id, user_id)

        await self.__attach_profile(user_report)

        return UserReport.model_validate(user_report)

    async def update_user_report(self, user_id: str, user_report: UpdateUserReport) -> UserReport:
        """
        Update an existing user report for a specific user.

        Args:
            user_id (str): UUID of the user updating the report.
            user_report (UpdateUserReportRequest): The updated report details.

        Returns:
            UserReport: The updated user report with attached profile information.
        """
        updated_user_report = await crud_provider.update(user_report.model_dump(), None, user_id)

        await self.__attach_profile(updated_user_report)

        return UserReport.model_validate(updated_user_report)

    async def delete_user_report(self, id: int, user_id: str) -> UserReport:
        """
        Delete a specific user report for a given user.

        Args:
            id (int): ID of the user report to delete.
            user_id (str): UUID of the user who owns the report.

        Returns:
            UserReport: The deleted user report with attached profile information.
        """
        deleted_user_report = await crud_provider.delete(id, user_id)

        await self.__attach_profile(deleted_user_report)

        return UserReport.model_validate(deleted_user_report)

    async def __attach_profile(self, user_report: dict) -> None:
        id = user_report.get('reported_user_id')
        level = await profiles_crud_provider.get(id)
        user_report['reported_user'] = level