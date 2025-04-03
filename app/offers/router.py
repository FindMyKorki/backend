from fastapi import APIRouter, Depends
from users.auth import authenticate_user

from .dataclasses import OfferResponse
from .service import OffersService

offers_router = APIRouter()
offers_service = OffersService()


@offers_router.get("/offers/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: int):
    return await offers_service.get_offers(offer_id)

# PUT /offers/{offer_id}

# POST /offers/{offer_id}:disable
# POST /offers/{offer_id}:enable

# GET /tutor-offers/{tutor_id}
# GET /tutor-offers/{offer_id}

# GET /active-offers/{tutor_id}
# GET /active-offers?sort_by=&order=
