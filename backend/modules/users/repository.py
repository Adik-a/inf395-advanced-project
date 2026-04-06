from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from modules.users.schemas import UsersSchema
from modules.users.models import UsersModel
from auth import hash_password


class UsersRepository:
    @classmethod
    async def check_user_exists(cls, user: UsersSchema, session: AsyncSession):
        data: UsersModel | None = await session.scalar(
            select(UsersModel).where(UsersModel.username == user.username)
        )
        return data

    @classmethod
    async def registrate_user(cls, user: UsersSchema, session: AsyncSession):
        hashed_password = hash_password(user.password)

        new_user = UsersModel(username=user.username, password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
