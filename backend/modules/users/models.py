from sqlalchemy.orm import Mapped, mapped_column

from database import Model


class UsersModel(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")
