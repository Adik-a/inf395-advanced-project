from typing import TYPE_CHECKING
from datetime import datetime

from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, UniqueConstraint

if TYPE_CHECKING:
    from modules.jobs.models import JobsModel
    from modules.users.models import UsersModel


class OffersModel(Model):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        default=datetime.utcnow,
    )
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    job: Mapped["JobsModel"] = relationship(back_populates="offers")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UsersModel"] = relationship(back_populates="offers")

    __table_args__ = (
        UniqueConstraint("user_id", "job_id"),
    )
