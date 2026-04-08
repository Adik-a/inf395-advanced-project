from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import OffersModel
from .schemas import OffersSchema


class OffersRepository:
    @classmethod
    async def create_offer(
        cls,
        user_id: int,
        job_id: int,
        offer_data: OffersSchema,
        session: AsyncSession,
    ):
        offer_data_dict = offer_data.model_dump()
        new_offer = OffersModel(
            **offer_data_dict,
            user_id=user_id,
            job_id=job_id,
        )
        session.add(new_offer)
        await session.commit()
        await session.refresh(new_offer)

        return new_offer

    @classmethod
    async def get_offers_by_job(
        cls,
        job_id: int,
        session: AsyncSession,
    ):
        data = await session.scalars(
            select(OffersModel)
            .where(OffersModel.job_id == job_id)
            .order_by(OffersModel.created_at.desc())
        )

        return data.all()

    @classmethod
    async def get_offers_by_user(
        cls,
        user_id: int,
        session: AsyncSession,
    ):
        data = await session.scalars(
            select(OffersModel)
            .where(OffersModel.user_id == user_id)
            .order_by(OffersModel.created_at.desc())
        )

        return data.all()

    @classmethod
    async def update_offer_status(
        cls,
        offer_id: int,
        status_update: str,
        session: AsyncSession,
    ):
        stmt = update(OffersModel).where(OffersModel.id == offer_id).values(status=status_update)
        

        await session.execute(stmt)
        await session.commit()

        return await session.get(OffersModel, offer_id)
