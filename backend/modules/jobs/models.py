from typing import TYPE_CHECKING
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, Interval, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Model

if TYPE_CHECKING:
    from modules.users.models import UsersModel
    from modules.offers.models import OffersModel


class JobsModel(Model):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(default=None, nullable=False)
    budget: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str | None] = mapped_column(default=None, nullable=True)
    status: Mapped[str] = mapped_column(default="open", nullable=False)
    duration: Mapped[timedelta | None] = mapped_column(Interval, nullable=True)
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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UsersModel"] = relationship(back_populates="jobs")

    offers: Mapped[list["OffersModel"]] = relationship(back_populates="job")
