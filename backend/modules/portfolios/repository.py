from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from modules.portfolios.schemas import (
    PortfoliosSchema,
    PortfoliosCreateSchema,
    PortfoliosUpdateSchema,
)
from modules.users.models import UsersModel
from .models import PortfoliosModel


class PortfoliosRepository:
    @classmethod
    async def create_portfolio(
        cls,
        user_id: int,
        portfolio_data: PortfoliosSchema,
        session: AsyncSession,
    ) -> PortfoliosCreateSchema:
        new_portfolio = PortfoliosModel(**portfolio_data.model_dump(), user_id=user_id)
        session.add(new_portfolio)
        await session.commit()
        await session.refresh(new_portfolio)

        return new_portfolio

    @classmethod
    async def get_user_portfolios(
        cls,
        user_id: int,
        session: AsyncSession,
    ):
        # data = await session.scalars(
        #     select(UsersModel)
        #     .where(UsersModel.id == user_id)
        #     .options(selectinload(UsersModel.portfolios))
        # )
        data = await session.scalars(
            select(PortfoliosModel).where(PortfoliosModel.user_id == user_id)
        )
        return data.all()

    @classmethod
    async def get_user_portfolio(
        cls,
        user_id: int,
        portfolio_id: int,
        session: AsyncSession,
    ):
        data = await session.scalar(
            select(PortfoliosModel).where(
                PortfoliosModel.user_id == user_id,
                PortfoliosModel.id == portfolio_id,
            )
        )
        return data

    @classmethod
    async def update_portfolio(
        cls,
        portfolio: PortfoliosModel,
        portfolio_update: PortfoliosUpdateSchema,
        session: AsyncSession,
        partial: bool = False,
    ):
        for field, value in portfolio_update.model_dump(exclude_unset=partial).items():
            if value is not None:
                setattr(portfolio, field, value)

        await session.commit()
        await session.refresh(portfolio)

        return portfolio

    @classmethod
    async def delete_portfolio(
        cls,
        portfolio: PortfoliosModel,
        session: AsyncSession,
    ):
        await session.delete(portfolio)
        await session.commit()
