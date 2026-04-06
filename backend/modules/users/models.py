from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database import Model


class UsersModel(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None] = mapped_column(default=None, nullable=True)
    password: Mapped[str | None] = mapped_column(default=None, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str | None] = mapped_column(default=None, nullable=True)
    bio: Mapped[str | None] = mapped_column(default=None, nullable=True)
    role: Mapped[str] = mapped_column(default="user")
    rating: Mapped[float] = mapped_column(default=0.0)
    is_oauth: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        default=datetime.utcnow,
    )
