from core.db_connection import supabase
from fastapi import HTTPException

from .dataclasses import OfferResponse, TutorOfferResponse, ActiveOfferResponse


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
        tutor_avatar_url=profile.get("avatar_url"),
        tutor_rating=tutor_profile.get("rating"),
        price=data.get("price"),
        subject_name=subject.get("name"),
        level=level.get("level"),
        icon_url=subject.get("icon_url"),
    )


def flatten_tutor_offers_data(data: list[dict]) -> list[TutorOfferResponse]:
    result = []
    for offer in data:
        result.append(flatten_tutor_offer_data(offer))

    return result


def flatten_tutor_offer_data(data: dict) -> TutorOfferResponse:
    subject = data.pop("subjects", {}) or {}
    level = data.pop("levels", {}) or {}
    result = TutorOfferResponse(
        id=data.get("id"),
        price=data.get("price"),
        subject_name=subject.get("name"),
        icon_url=subject.get("icon_url"),
        level=level.get("level"),
        is_active=data.get("is_active")
    )

    return result


def flatten_active_offers(data: list[dict]) -> list[ActiveOfferResponse]:
    result = []
    for offer in data:
        tutor_profile = offer.pop("tutor_profiles", {}) or {}
        profile = tutor_profile.pop("profiles", {}) or {}
        subject = offer.pop("subjects", {}) or {}
        level = offer.pop("levels", {}) or {}
        result.append(
            ActiveOfferResponse(
                id=offer.get("id"),
                tutor_full_name=profile.get("full_name", "Unknown"),
                tutor_avatar_url=profile.get("avatar_url"),
                tutor_rating=tutor_profile.get("rating"),
                price=offer.get("price"),
                subject_name=subject.get("name"),
                icon_url=subject.get("icon_url"),
                level=level.get("level"),
            )
        )

    return result
