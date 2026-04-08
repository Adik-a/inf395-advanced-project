from fastapi import APIRouter, Depends

from auth import get_current_user
from database import SessionDep
from modules.offers.schemas import OffersSchema
from modules.offers.repository import OffersRepository

router = APIRouter(
    prefix="/offers",
    tags=["Offers"],
)


@router.get("/me")
async def get_my_offers(
    session: SessionDep,
    current_url: dict = Depends(get_current_user),
):
    offers_data = await OffersRepository.get_offers_by_user(
        user_id=current_url["sub"],
        session=session,
    )

    return {
        "offers": offers_data,
    }
