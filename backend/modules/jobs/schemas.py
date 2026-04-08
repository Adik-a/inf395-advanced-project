from datetime import timedelta

from pydantic import BaseModel


class JobsSchema(BaseModel):
    title: str
    description: str
    budget: float
    category: str | None = None
    duration: int | None = None


class JobsUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    budget: float | None = None
    category: str | None = None
    duration: int | None = None
