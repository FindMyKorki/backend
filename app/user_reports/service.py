from core.db_connection import supabase
from fastapi import HTTPException
from .dataclasses import UserReport, CreateUserReport


class UserReportsService:
    async def create_user_report(self, reported_user_id: str, report: CreateUserReport, reporter_id: str) -> str:
        """Create a new user report"""
        # Verify the reported user exists
        try:
            user = supabase.auth.admin.get_user_by_id(reported_user_id).user
        except:
            raise HTTPException(status_code=404, detail="Reported user not found")
            
        report_data = report.model_dump()
        report_data["user_id"] = reporter_id
        report_data["reported_user_id"] = reported_user_id
        
        result = (
            supabase.table("user_reports")
            .insert(report_data)
            .execute()
        )
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create user report")
            
        return f"User report created with ID: {result.data[0]['id']}"