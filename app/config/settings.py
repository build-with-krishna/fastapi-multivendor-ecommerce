from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None

    class Config:
        env_file = BASE_DIR / ".env"
        extra = "ignore"

settings = Settings()