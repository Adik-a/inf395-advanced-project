from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from modules.users.schemas import UsersSchema
from modules.users.models import UsersModel
from auth import hash_password, verify_password


class UsersRepository:
    @classmethod
    async def login_user(cls, user: UsersSchema, session: AsyncSession):
        data = await session.execute(
            select(UsersModel).where(UsersModel.username == user.username)
        )
        data = data.scalars().first()

        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
            )

        if not verify_password(user.password, data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
            )

        return data

    @classmethod
    async def registrate_user(cls, user: UsersSchema, session: AsyncSession):
        data = await session.execute(
            select(UsersModel).where(UsersModel.username == user.username)
        )
        data = data.scalars().first()

        if data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        hashed_password = hash_password(user.password)

        new_user = UsersModel(username=user.username, password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return {"message": "User created successfully"}
