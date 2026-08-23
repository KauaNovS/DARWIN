# core/config.py
#
# NOTE: Not present in the original plan document — added as minimal glue
# code so `main.py` and the services that do `from core.config import
# settings` actually import. Fill in / extend as needed.
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Darwin Genesis API"
    ENV: str = "development"

    DATABASE_URL: str = "postgresql+asyncpg://darwin:darwin123@localhost:5432/darwin"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "darwin123"
    REDIS_URL: str = "redis://localhost:6379"

    OPENAI_API_KEY: str = ""

    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
