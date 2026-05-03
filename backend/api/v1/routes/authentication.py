import os

from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from modules.users.schemas import UsersSchema, GoogleTokenSchema
from auth import create_access_token, verify_password
from database import SessionDep
from modules.users.repository import UsersRepository
from config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

GOOGLE_CLIENT_ID = settings.client_id


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    # response: Response,
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_data = await UsersRepository.get_user_by_email(
        email=form_data.username,
        session=session,
    )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
        )

    if not user_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registered via Google. Please use Google Login.",
        )

    if not verify_password(form_data.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
        )

    token = create_access_token({"sub": str(user_data.id), "role": user_data.role})

    # response.set_cookie(
    #     key="access_token",
    #     value=f"Bearer {token}",
    #     httponly=True,
    #     secure=True,
    #     samesite="none",
    #     domain=None,
    # )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_data.id,
            "email": user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
        },
    }
    # return {"msg": "Logged in"}


@router.post("/register", status_code=status.HTTP_200_OK)
async def registration_user(
    user: UsersSchema,
    session: SessionDep,
):
    user_data = await UsersRepository.get_user_by_email(
        email=user.email,
        session=session,
    )

    if user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    new_user = await UsersRepository.registrate_user(user, session)
    return {"message": "User created successfully", "user": new_user}


@router.post("/google", status_code=status.HTTP_200_OK)
async def auth_via_google(
    # response: Response,
    payload: GoogleTokenSchema,
    session: SessionDep,
):
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.token, google_requests.Request(), GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        google_id = idinfo.get("sub")
        # name = idinfo.get("name")

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token"
        )

    user_data = await UsersRepository.get_user_by_email(email=email, session=session)

    if not user_data:
        new_google_user = UsersSchema(
            email=email,
            first_name=idinfo.get("given_name"),
            last_name=idinfo.get("family_name"),
            password=None,
        )
        if new_google_user.first_name is None:
            if idinfo.get("name"):
                new_google_user.first_name = idinfo.get("name")
            else:
                new_google_user.first_name = email.split("@")[0]

        user_data = await UsersRepository.registrate_user(
            user=new_google_user,
            session=session,
            is_oauth=True,
        )

    token = create_access_token({"sub": str(user_data.id), "role": user_data.role})

    # response.set_cookie(
    #     key="access_token",
    #     value=f"Bearer {token}",
    #     httponly=True,
    #     secure=True,
    #     samesite="none",
    #     domain=None,
    # )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_data.id,
            "email": user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
        },
    }
    # return {"msg": "Logged in"}
