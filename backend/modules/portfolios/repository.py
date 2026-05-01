from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from modules.portfolios.schemas import (
    PortfoliosSchema,
    PortfoliosCreateSchema,
    PortfoliosUpdateSchema,
)
from modules.users.models import UsersModel
from .models import PortfoliosModel, FAQsModel, RequirementsModel


class PortfoliosRepository:
    @classmethod
    async def create_portfolio(
        cls,
        user_id: int,
        portfolio_data: PortfoliosSchema,
        session: AsyncSession,
    ) -> PortfoliosCreateSchema:
        portfolio_data = portfolio_data.model_dump()
        faqs = portfolio_data.pop("faqs", [])
        requirements = portfolio_data.pop("requirements", [])

        if portfolio_data["pricing_mode"] == "one":
            del portfolio_data["price_standard"]
            del portfolio_data["price_premium"]
            del portfolio_data["package_name_standard"]
            del portfolio_data["package_name_premium"]
            del portfolio_data["description_standard"]
            del portfolio_data["description_premium"]
            del portfolio_data["delivery_standard"]
            del portfolio_data["delivery_premium"]
            del portfolio_data["revisions_standard"]
            del portfolio_data["revisions_premium"]
        else:
            portfolio_data["price_standard"] = int(
                float(portfolio_data["price_standard"])
            )
            portfolio_data["price_premium"] = int(
                float(portfolio_data["price_premium"])
            )

        portfolio_data["price_basic"] = int(float(portfolio_data["price_basic"]))

        new_portfolio = PortfoliosModel(**portfolio_data, user_id=user_id)
        session.add(new_portfolio)
        await session.commit()
        await session.refresh(new_portfolio)

        await cls.create_faqs(
            portfolio_id=new_portfolio.id,
            faqs_data=faqs,
            session=session,
        )

        await cls.create_requirements(
            portfolio_id=new_portfolio.id,
            requirements_data=requirements,
            session=session,
        )

        return new_portfolio

    @classmethod
    async def create_faqs(
        cls,
        portfolio_id: int,
        faqs_data: list,
        session: AsyncSession,
    ):
        new_faqs = [FAQsModel(**faq, portfolio_id=portfolio_id) for faq in faqs_data]
        session.add_all(new_faqs)
        await session.commit()

    @classmethod
    async def create_requirements(
        cls,
        portfolio_id: int,
        requirements_data: list,
        session: AsyncSession,
    ):
        new_requirements = [
            RequirementsModel(**req, portfolio_id=portfolio_id)
            for req in requirements_data
        ]
        session.add_all(new_requirements)
        await session.commit()

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
        query = select(
            PortfoliosModel.id,
            PortfoliosModel.title,
            PortfoliosModel.initial_status,
            PortfoliosModel.price_basic,
            PortfoliosModel.category,
            PortfoliosModel.images,
        ).where(PortfoliosModel.user_id == user_id)

        data = await session.execute(query)
        return data.mappings().all()

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
