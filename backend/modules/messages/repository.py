from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import MessagesModel
from modules.users.models import UsersModel


class MessagesRepository:
    @classmethod
    async def create_message(
        cls,
        sender_id: int,
        receiver_id: str,
        content: str,
        session: AsyncSession,
    ) -> MessagesModel:
        sender_email = await session.scalar(
            select(UsersModel.email).where(UsersModel.id == sender_id)
        )
        receiver_email = await session.scalar(
            select(UsersModel.email).where(UsersModel.id == receiver_id)
        )
        # receiver_id = await session.scalar(
        #     select(UsersModel.id).where(UsersModel.email == receiver_email)
        # )

        new_message = MessagesModel(
            sender_id=sender_id,
            receiver_id=receiver_id,
            sender_email=sender_email,
            receiver_email=receiver_email,
            content=content,
        )
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)

        return new_message

    @classmethod
    async def get_messages_between_users(
        cls,
        user1_id: int,
        user2_email: str,
        session: AsyncSession,
    ) -> list[MessagesModel]:
        result = await session.execute(
            select(MessagesModel)
            .where(
                (
                    (MessagesModel.sender_id == user1_id)
                    & (MessagesModel.receiver_email == user2_email)
                )
                | (
                    (MessagesModel.sender_email == user2_email)
                    & (MessagesModel.receiver_id == user1_id)
                )
            )
            .order_by(MessagesModel.created_at)
        )
        return result.scalars().all()

    @classmethod
    async def get_my_all_messages(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[MessagesModel]:
        result = await session.execute(
            select(MessagesModel)
            # .where(
            #     (MessagesModel.sender_id == user_id)
            #     | (MessagesModel.receiver_id == user_id)
            # )
            .order_by(MessagesModel.created_at)
        )
        return result.scalars().all()
    
    @classmethod
    async def get_user_by_email(
        cls,
        email: str,
        session: AsyncSession,
    ) -> UsersModel | None:
        result = await session.execute(
            select(UsersModel).where(UsersModel.email == email)
        )
        return result.scalar_one_or_none()