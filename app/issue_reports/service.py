from core.db_connection import supabase
from crud.crud_provider import CRUDProvider
from fastapi import HTTPException

from .dataclasses import IssueReport, IssueReport2, BaseIssueReport, CreateIssueReport

crud_provider = CRUDProvider('issue_reports', 'user_id')


class IssueReportsService:

    async def create_issue_report(self, report: CreateIssueReport, user_id: str) -> str:
        """Create a new issue report"""
        issue_data = report.model_dump()
        issue_data["user_id"] = user_id

        result = (
            supabase.table("issue_reports")
            .insert(issue_data)
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create issue report")

        return f"Issue report created with ID: {result.data[0]['id']}"

    # CRUD
    async def create_issue_report2(self, user_id: str, issue_report: BaseIssueReport) -> IssueReport2:
        """
        Create a new issue report submitted by a user.

        Args:
            user_id (str): UUID of the user submitting the report.
            issue_report (BaseIssueReport): The issue report details.

        Returns:
            IssueReport2: The created issue report record.
        """
        issue_report = issue_report.model_dump()
        issue_report['user_id'] = user_id

        new_issue_report = await crud_provider.create(issue_report)

        return IssueReport2.model_validate(new_issue_report)

    async def get_issue_report(self, id: int, user_id: str) -> IssueReport2:
        """
        Retrieve a specific issue report by ID for a given user.

        Args:
            id (int): ID of the issue report to retrieve.
            user_id (str): UUID of the user who owns the report.

        Returns:
            IssueReport2: The requested issue report record.
        """
        issue_report = await crud_provider.get(id, user_id)

        return IssueReport2.model_validate(issue_report)

    async def update_issue_report(self, user_id: str, issue_report: IssueReport2) -> IssueReport2:
        """
        Update an existing issue report for a user.

        Args:
            user_id (str): UUID of the user updating the report.
            issue_report (IssueReport): The updated issue report data.

        Returns:
            IssueReport2: The updated issue report record.
        """
        updated_issue_report = await crud_provider.update(issue_report.model_dump(), None, user_id)

        return IssueReport2.model_validate(updated_issue_report)

    async def delete_issue_report(self, id: int, user_id: str) -> IssueReport2:
        """
        Delete a specific issue report for a given user.

        Args:
            id (int): ID of the issue report to delete.
            user_id (str): UUID of the user who owns the report.

        Returns:
            IssueReport2: The deleted issue report record.
        """
        deleted_issue_report = await crud_provider.delete(id, user_id)

        return IssueReport2.model_validate(deleted_issue_report)
