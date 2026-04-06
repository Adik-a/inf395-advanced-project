from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from modules.users.schemas import UsersSchema
from auth import create_access_token, verify_password
from database import SessionDep
from modules.users.repository import UsersRepository

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_data = await UsersRepository.check_user_exists(user=form_data, session=session)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
        )

    if not verify_password(form_data.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
        )

    token = create_access_token({"sub": str(user_data.id), "role": user_data.role})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_200_OK)
async def registration_user(
    user: UsersSchema,
    session: SessionDep,
):
    user_data = await UsersRepository.check_user_exists(user=user, session=session)

    if user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    new_user = await UsersRepository.registrate_user(user, session)
    return {"message": "User created successfully", "user": new_user}
