from pydantic import BaseModel, Field, ConfigDict

class UsersSchema(BaseModel):
    username: str
    password: str