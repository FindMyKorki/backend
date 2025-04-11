from core.db_connection import supabase
from fastapi import HTTPException
from datetime import datetime
from .dataclasses import CreateOfferReport

class OfferReportsService:
    async def create_offer_report(self, offer_id: int, report: CreateOfferReport, user_id: str) -> str:
        """Create a new user report related to an offer"""
        offer = supabase.table("offers").select("*").eq("id", offer_id).execute()
        
        if not offer.data or len(offer.data) == 0:
            raise HTTPException(status_code=404, detail="Offer not found")
            
        tutor_id = offer.data[0]["tutor_id"]
        
        report_data = {
            "user_id": user_id,  
            "reported_user_id": tutor_id,  
            "reason": "offer related",  
            "message": f"Offer ID: {offer_id}\nMessage: {report.message}"  
        }
        
        result = supabase.table("user_reports").insert(report_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create user report")
            
        return f"User report created with ID: {result.data[0]['id']}"