from fastapi import APIRouter, Depends, HTTPException, status

from database import SessionDep
from modules.users.schemas import (
    UsersSchema,
    UsersMineSchema,
    UsersOthersSchema,
    UsersUpdateSchema,
)
from modules.users.repository import UsersRepository
from auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def get_user(
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
) -> UsersMineSchema:
    user_data = await UsersRepository.get_user_by_id(
        current_user["sub"],
        session=session,
    )
    return user_data


@router.patch("/me")
async def update_user(
    user_update: UsersUpdateSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
) -> UsersMineSchema:
    user_data = await UsersRepository.get_user_by_id(
        current_user["sub"],
        session=session,
    )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user_data.username and user_update.username:
        is_username_taken = await UsersRepository.get_user_by_username(
            user_update.username,
            session=session,
        )
        if is_username_taken and is_username_taken.id != user_data.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

    updated_user = await UsersRepository.update_user(
        session=session,
        user=user_data,
        user_update=user_update,
        partial=True,
    )
    return updated_user


@router.get("/{user_id}")
async def get_user_by_id(
    session: SessionDep,
    user_id: int,
    current_user: dict = Depends(get_current_user),
) -> UsersOthersSchema:
    user_data = await UsersRepository.get_user_by_id(
        user_id,
        session=session,
    )
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user_data
