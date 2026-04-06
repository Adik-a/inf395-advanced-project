from fastapi import APIRouter, status, HTTPException, Depends

from auth import get_any_user, get_admin_user
from modules.users.schemas import UsersSchema
from database import SessionDep
from modules.users.repository import UsersRepository

router = APIRouter(prefix="/registration", tags=["Registration"])


@router.post("", status_code=status.HTTP_200_OK)
async def registration_user(user: UsersSchema, session: SessionDep):
    msg = await UsersRepository.registrate_user(user, session)
    return msg
