from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from modules.users.schemas import UsersFullSchema, UsersSchema, UsersUpdateSchema
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
    async def get_user_by_id(cls, user_id: int, session: AsyncSession):
        data: UsersModel | None = await session.scalar(
            select(UsersModel).where(UsersModel.id == user_id)
        )
        return data

    @classmethod
    async def registrate_user(
        cls,
        user: UsersSchema,
        session: AsyncSession,
        is_oauth: bool = False,
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

    @classmethod
    async def update_user(
        cls,
        session: AsyncSession,
        user: UsersFullSchema,
        user_update: UsersUpdateSchema,
        partial: bool = False,
    ):
        for name, value in user_update.model_dump(exclude_unset=partial).items():
            if name == "password" and value is not None:
                value = hash_password(value)
            setattr(user, name, value)
        await session.commit()
        await session.refresh(user)
        return user
