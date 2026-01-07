from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:ebimobowei81@localhost/neco_db"
    SECRET_KEY: str = "neco_staff_secret_key_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    SUPER_ADMIN_USERNAME: str = "admin"
    SUPER_ADMIN_PASSWORD: str = "admin_password"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
