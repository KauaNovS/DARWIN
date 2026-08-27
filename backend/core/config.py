from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://darwin:darwin@localhost/darwin"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "darwin"
    REDIS_URL: str = "redis://localhost:6379"
    SECRET_KEY: str = "darwin-secret-mude-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    OPENAI_API_KEY: str = ""
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8081"]

    class Config:
        env_file = ".env"

settings = Settings()
