from .dataclasses import IssueReport, BaseIssueReport
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('issue_reports', 'user_id')


class IssueReportsService:

    async def create_issue_report(self, user_id: str, issue_report: BaseIssueReport) -> IssueReport:
        """
        Create a new issue report submitted by a user.

        Args:
            user_id (str): UUID of the user submitting the report.
            issue_report (BaseIssueReport): The issue report details.

        Returns:
            IssueReport: The created issue report record.
        """
        issue_report = issue_report.model_dump()
        issue_report['user_id'] = user_id

        new_issue_report = await crud_provider.create(issue_report)

        return IssueReport.model_validate(new_issue_report)

    async def get_issue_report(self, id: int, user_id: str) -> IssueReport:
        """
        Retrieve a specific issue report by ID for a given user.

        Args:
            id (int): ID of the issue report to retrieve.
            user_id (str): UUID of the user who owns the report.

        Returns:
            IssueReport: The requested issue report record.
        """
        issue_report = await crud_provider.get(id, user_id)

        return IssueReport.model_validate(issue_report)

    async def update_issue_report(self, user_id: str, issue_report: IssueReport) -> IssueReport:
        """
        Update an existing issue report for a user.

        Args:
            user_id (str): UUID of the user updating the report.
            issue_report (IssueReport): The updated issue report data.

        Returns:
            IssueReport: The updated issue report record.
        """
        updated_issue_report = await crud_provider.update(issue_report.model_dump(), None, user_id)

        return IssueReport.model_validate(updated_issue_report)

    async def delete_issue_report(self, id: int, user_id: str) -> IssueReport:
        """
        Delete a specific issue report for a given user.

        Args:
            id (int): ID of the issue report to delete.
            user_id (str): UUID of the user who owns the report.

        Returns:
            IssueReport: The deleted issue report record.
        """
        deleted_issue_report = await crud_provider.delete(id, user_id)

        return IssueReport.model_validate(deleted_issue_report)
