from core.db_connection import supabase
from fastapi import HTTPException
from .dataclasses import OfferReport, CreateOfferReport


class OfferReportsService:
    async def create_offer_report(self, offer_id: int, report: CreateOfferReport, user_id: str) -> str:
        """Create a new offer report"""
        # Verify the offer exists
        offer = (
            supabase.table("offers")
            .select("*")
            .eq("id", offer_id)
            .execute()
        )
        
        if not offer.data or len(offer.data) == 0:
            raise HTTPException(status_code=404, detail="Offer not found")
            
        report_data = report.model_dump()
        report_data["user_id"] = user_id
        report_data["offer_id"] = offer_id
        
        result = (
            supabase.table("offer_reports")
            .insert(report_data)
            .execute()
        )
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create offer report")
            
        return f"Offer report created with ID: {result.data[0]['id']}"