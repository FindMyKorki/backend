from .dataclasses import IssueReport, CreateIssueReportRequest, UpdateIssueReportRequest
from crud.crud_provider import CRUDProvider


crud_provider = CRUDProvider('issue_reports', 'user_id')


class IssueReportsService:
    async def create_issue_report(self, user_id: str, issue_report: CreateIssueReportRequest) -> IssueReport:
        issue_report = issue_report.model_dump()
        issue_report['user_id'] = user_id

        new_issue_report = await crud_provider.create(issue_report)

        return IssueReport.model_validate(new_issue_report)

    async def get_issue_report(self, id: int, user_id: str) -> IssueReport:
        issue_report: dict = await crud_provider.get(id, user_id)

        return IssueReport.model_validate(issue_report)

    async def update_issue_report(self, user_id, issue_report: UpdateIssueReportRequest) -> IssueReport:
        updated_issue_report = await crud_provider.update(issue_report.model_dump(exclude='id'), issue_report.id, user_id)

        return IssueReport.model_validate(updated_issue_report)

    async def delete_issue_report(self, id: int, user_id: str) -> IssueReport:
        deleted_issue_report = await crud_provider.delete(id, user_id)

        return IssueReport.model_validate(deleted_issue_report)
