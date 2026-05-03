from fastapi import APIRouter, Depends, status

from modules.portfolios.schemas import (
    PortfoliosSchema,
    PortfoliosUpdateSchema,
)
from modules.portfolios.repository import PortfoliosRepository
from database import SessionDep
from auth import get_current_user

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio_data: PortfoliosSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    new_portfolio = await PortfoliosRepository.create_portfolio(
        user_id=current_user["sub"],
        portfolio_data=portfolio_data,
        session=session,
    )
    return {
        "msg": "Portfolio created successfully",
        "portfolio": new_portfolio,
    }


@router.get("/me")
async def get_my_portfolios(
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    portfolios = await PortfoliosRepository.get_user_portfolios(
        user_id=current_user["sub"],
        session=session,
    )

    if not portfolios:
        return {"msg": "No portfolios found for this user"}

    return portfolios


@router.get("/user/{portfolio_id}")
async def get_portfolio_by_id(
    portfolio_id: int,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    data = await PortfoliosRepository.get_portfolio_by_id(
        portfolio_id=portfolio_id,
        session=session,
    )

    if not data:
        return {"msg": "Portfolio not found"}

    return data


@router.get("/{user_id}")
async def get_user_portfolios(
    user_id: int,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    portfolios = await PortfoliosRepository.get_user_portfolios(
        user_id=user_id,
        session=session,
    )

    if not portfolios:
        return {"msg": "No portfolios found for this user"}

    return portfolios


@router.get("/category/{category}")
async def get_portfolios_by_category(
    category: str,
    session: SessionDep,
    subcategory: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
):
    portfolios = await PortfoliosRepository.get_portfolios_by_category(
        category=category,
        session=session,
        subcategory=subcategory,
    )
    return portfolios


@router.get("/{user_id}/{portfolio_id}")
async def get_user_portfolio(
    user_id: int,
    portfolio_id: int,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    portfolio = await PortfoliosRepository.get_user_portfolio(
        user_id=user_id,
        portfolio_id=portfolio_id,
        session=session,
    )

    if not portfolio:
        return {"msg": "Portfolio not found"}

    return portfolio


@router.put("/change/{portfolio_id}", status_code=status.HTTP_200_OK)
async def update_user_portfolio(
    portfolio_id: int,
    portfolio_update: PortfoliosSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    portfolio = await PortfoliosRepository.get_user_portfolio(
        user_id=current_user["sub"],
        portfolio_id=portfolio_id,
        session=session,
    )

    if not portfolio:
        return {"msg": "Portfolio not found"}

    updated_portfolio = await PortfoliosRepository.update_portfolio(
        portfolio=portfolio,
        portfolio_data=portfolio_update,
        user_id=current_user["sub"],
        session=session,
        partial=True,
    )

    return {
        "msg": "Portfolio updated successfully",
        "portfolio": updated_portfolio,
    }


@router.delete("/delete/{portfolio_id}")
async def delete_user_portfolio(
    portfolio_id: int,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    portfolio = await PortfoliosRepository.get_user_portfolio(
        user_id=current_user["sub"],
        portfolio_id=portfolio_id,
        session=session,
    )

    if not portfolio:
        return {"msg": "Portfolio not found"}

    await PortfoliosRepository.delete_portfolio(
        portfolio=portfolio,
        session=session,
    )

    return {"msg": "Portfolio deleted successfully"}
