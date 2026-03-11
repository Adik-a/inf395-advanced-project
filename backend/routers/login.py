from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UsersSchema
from auth import create_access_token

from database import SessionDep
from repositories.users import UsersRepository

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def login_user(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = await UsersRepository.login_user(form_data, session)
    token = create_access_token({"sub": str(user_data.id), "role": user_data.role})

    # return {"access_token": token, "token_type": "bearer"}
    return {"msg": "Login successful"}