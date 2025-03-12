from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Email Marketing API"
    API_V1_STR: str = "/api/v1"
    
    # SendGrid
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://sushil:1234@localhost:5432/xxx"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()