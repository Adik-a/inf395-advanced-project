from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UsersSchema(BaseModel):
    email: EmailStr
    password: str | None = None
    first_name: str
    last_name: str | None = None


class UsersMineSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None
    rating: float
    location: str | None = None
    about_me: str | None = None
    skills: str | None = None
    created_at: datetime


class UsersOthersSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    email: str
    username: str | None = None
    bio: str | None = None
    rating: float


class UsersUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    bio: str | None = None
    location: str | None = None
    about_me: str | None = None
    skills: str | None = None


class GoogleTokenSchema(BaseModel):
    token: str
