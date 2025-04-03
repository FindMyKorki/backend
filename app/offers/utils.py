from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import OfferResponse


def get_offers(offer_id: int) -> list[OfferResponse]:
    offers = (
        supabase.table('offers')
        .select("id, description, price, tutor_profiles(rating, profiles(full_name))")
        .eq("id", offer_id)
        .all()
    )

    if offers.data and len(offers.data) > 0:
        return flatten_offers_data(offers.data)

    return None


def flatten_offer_data(data: dict) -> OfferResponse:
    tutor_profile = data.pop("tutor_profiles", {}) or {}
    profile = tutor_profile.pop("profiles", {}) or {}
    subject = data.pop("subjects", {}) or {}
    level = data.pop("levels", {}) or {}

    return OfferResponse(
        id=data["id"],
        description=data.get("description"),
        tutor_full_name=profile.get("full_name", "Unknown"),
        tutor_url=None,  # Domyślnie `None`
        tutor_rating=tutor_profile.get("rating"),
        price=data.get("price"),
        subject_name=subject.get("name"),
        level=level.get("level"),
        icon_url=subject.get("icon_url"),
    )
