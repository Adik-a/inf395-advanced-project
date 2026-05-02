from datetime import datetime

from pydantic import BaseModel


class MessagesSchema(BaseModel):
    sender_id: int
    receiver_email: str
    content: str

class MessagesCreateSchema(MessagesSchema):
    id: int
    created_at: datetime