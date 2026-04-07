from pydantic import BaseModel


class PortfoliosSchema(BaseModel):
    title: str
    description: str
    price: float | None


class PortfoliosCreateSchema(PortfoliosSchema):
    user_id: int


class PortfoliosUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
