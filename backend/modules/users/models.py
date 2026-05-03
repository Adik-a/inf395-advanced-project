from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Model

if TYPE_CHECKING:
    from modules.portfolios.models import PortfoliosModel
    from modules.jobs.models import JobsModel
    from modules.offers.models import OffersModel


class UsersModel(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None] = mapped_column(
        default=None, nullable=True, unique=True
    )
    password: Mapped[str | None] = mapped_column(default=None, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str | None] = mapped_column(default=None, nullable=True)
    bio: Mapped[str | None] = mapped_column(default=None, nullable=True)
    location: Mapped[str | None] = mapped_column(default=None, nullable=True)
    about_me: Mapped[str | None] = mapped_column(default=None, nullable=True)
    skills: Mapped[str | None] = mapped_column(default=None, nullable=True)

    role: Mapped[str] = mapped_column(default="user")
    rating: Mapped[float] = mapped_column(default=0.0)
    is_oauth: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        default=datetime.utcnow,
    )
    portfolios: Mapped[list["PortfoliosModel"]] = relationship(back_populates="user")
    jobs: Mapped[list["JobsModel"]] = relationship(back_populates="user")
    offers: Mapped[list["OffersModel"]] = relationship(back_populates="user")
