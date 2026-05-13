import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://medicore:secret@db:5432/medicore")
    postgres_user: str = os.getenv("POSTGRES_USER", "medicore")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "secret")
    postgres_db: str = os.getenv("POSTGRES_DB", "medicore")
    postgres_host: str = os.getenv("POSTGRES_HOST", "db")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    secret_key: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    algorithm: str = os.getenv("ALGORITHM", "HS256")


settings = Settings()
