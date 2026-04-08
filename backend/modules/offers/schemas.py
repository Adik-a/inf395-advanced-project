from pydantic import BaseModel

class OffersSchema(BaseModel):
    letter: str
    price: float | None = None

class OffersStatusUpdateSchema(BaseModel):
    status: str