from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from modules.users.schemas import UsersSchema
from modules.users.models import UsersModel
from auth import hash_password


class UsersRepository:
    @classmethod
    async def get_user_by_email(cls, email: str, session: AsyncSession):
        data: UsersModel | None = await session.scalar(
            select(UsersModel).where(UsersModel.email == email)
        )
        return data

    @classmethod
    async def registrate_user(
        cls, user: UsersSchema, session: AsyncSession, is_oauth: bool = False
    ):
        if user.password:
            hashed_password = hash_password(user.password)
        else:
            hashed_password = None

        new_user = UsersModel(
            email=user.email,
            password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            is_oauth=is_oauth,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
