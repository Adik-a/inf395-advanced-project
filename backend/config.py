import re

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    database_url: str
    secret_key: str
    client_id: str
    client_secret: str

    @field_validator("database_url", mode="before")
    @classmethod
    def force_asyncpg_dialect(cls, v: str) -> str:
        """Rewrite postgresql:// or postgres:// to postgresql+asyncpg://
        so SQLAlchemy always uses the asyncpg driver that is installed,
        regardless of what the DATABASE_URL environment variable contains.
        """
        return re.sub(r"^postgres(?:ql)?://", "postgresql+asyncpg://", v)


settings = Settings()
