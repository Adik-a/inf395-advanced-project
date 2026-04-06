import os

from fastapi import APIRouter, status, HTTPException, Depends
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

    # Проверка: если пользователь зарегистрирован через Google, у него может не быть пароля
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

    return {"access_token": token, "token_type": "bearer"}


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
    payload: GoogleTokenSchema,
    session: SessionDep,
):
    try:
        # 1. Проверяем токен в Google
        idinfo = id_token.verify_oauth2_token(
            payload.token, google_requests.Request(), GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        google_id = idinfo.get("sub")
        # name = idinfo.get("name") # Можно также извлечь имя или аватарку

    except ValueError:
        # Токен недействителен (просрочен, подделан и т.д.)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token"
        )

    # 2. Ищем пользователя по email в базе
    user_data = await UsersRepository.get_user_by_email(email=email, session=session)

    # 3. Если пользователя нет - регистрируем его
    if not user_data:
        # Создаем DTO/схему для регистрации через Google
        # Пароль оставляем пустым, либо генерируем случайный (в зависимости от вашей БД)
        new_google_user = UsersSchema(
            email=email,
            first_name=idinfo.get("given_name"),  # Берем имя из токена
            last_name=idinfo.get("family_name"),  # Берем фамилию из токена
            password=None,  # Важно учесть это в модели БД (nullable=True)
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

    # 4. Генерируем наш стандартный внутренний токен приложения
    token = create_access_token({"sub": str(user_data.id), "role": user_data.role})

    return {"access_token": token, "token_type": "bearer"}
