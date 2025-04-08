from core.db_connection import supabase
from fastapi import HTTPException
from .dataclasses import IssueReport, CreateIssueReport


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