from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UsersSchema(BaseModel):
    email: EmailStr
    password: str | None = None
    first_name: str
    last_name: str | None = None


class UsersRegisterSchema(UsersSchema):
    pass


class GoogleTokenSchema(BaseModel):
    token: str
