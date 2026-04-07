from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UsersSchema(BaseModel):
    email: EmailStr
    password: str | None = None
    first_name: str
    last_name: str | None = None


class UsersFullSchema(UsersSchema):
    username: str | None = None
    bio: str | None = None


class UsersMineSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None
    rating: float


class UsersOthersSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None
    rating: float


class UsersUpdateSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None


class GoogleTokenSchema(BaseModel):
    token: str
