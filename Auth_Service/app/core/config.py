from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    BACKEND_CORS_ORIGINS: str = "*"  # default as string
    GMAIL_USER: str
    GMAIL_APP_PASSWORD: str

    @property
    def cors_origins(self) -> List[str]:
        if self.BACKEND_CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"

Settings = Settings()