from pydantic_settings import BaseSettings, SettingsConfigDict
import cloudinary
import cloudinary.uploader


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    database_url: str
    secret_key: str
    client_id: str
    client_secret: str
    cloud_name: str
    cloud_api_key: str
    cloud_api_secret: str


settings = Settings()

cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.cloud_api_key,
    api_secret=settings.cloud_api_secret,
    secure=True,
)
