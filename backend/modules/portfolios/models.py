from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ARRAY, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Model

if TYPE_CHECKING:
    from modules.users.models import UsersModel


class PortfoliosModel(Model):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UsersModel"] = relationship(back_populates="portfolios")

    title: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    subcategory: Mapped[str] = mapped_column(nullable=False)
    initial_status: Mapped[str] = mapped_column(nullable=False)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    pricing_mode: Mapped[str] = mapped_column(nullable=False)
    price_basic: Mapped[int] = mapped_column(nullable=False)
    price_standard: Mapped[int | None] = mapped_column(default=None, nullable=True)
    price_premium: Mapped[int | None] = mapped_column(default=None, nullable=True)

    package_name_basic: Mapped[str] = mapped_column(nullable=False)
    package_name_standard: Mapped[str | None] = mapped_column(
        default=None, nullable=True
    )
    package_name_premium: Mapped[str | None] = mapped_column(
        default=None, nullable=True
    )

    description_basic: Mapped[str] = mapped_column(nullable=False)
    description_standard: Mapped[str | None] = mapped_column(
        default=None, nullable=True
    )
    description_premium: Mapped[str | None] = mapped_column(default=None, nullable=True)

    delivery_basic: Mapped[str] = mapped_column(nullable=False)
    delivery_standard: Mapped[str | None] = mapped_column(default=None, nullable=True)
    delivery_premium: Mapped[str | None] = mapped_column(default=None, nullable=True)

    revisions_basic: Mapped[str] = mapped_column(nullable=False)
    revisions_standard: Mapped[str | None] = mapped_column(default=None, nullable=True)
    revisions_premium: Mapped[str | None] = mapped_column(default=None, nullable=True)

    description: Mapped[str] = mapped_column(nullable=False)

    faqs: Mapped[list["FAQsModel"]] = relationship(back_populates="portfolio")
    requirements: Mapped[list["RequirementsModel"]] = relationship(
        back_populates="portfolio"
    )
    images: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        default=datetime.utcnow,
    )


class FAQsModel(Model):
    __tablename__ = "faqs"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)

    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    portfolio: Mapped["PortfoliosModel"] = relationship(back_populates="faqs")


class RequirementsModel(Model):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    requirement: Mapped[str] = mapped_column(nullable=False)
    is_required: Mapped[bool] = mapped_column(nullable=False)

    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    portfolio: Mapped["PortfoliosModel"] = relationship(back_populates="requirements")
