from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Parfum App"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]  # Frontend URL
    
    # PostgreSQL Database settings
    POSTGRES_SERVER: str = "localhost"  # If using Docker, this should match your service name
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "mydatabase"
    POSTGRES_PORT: str = "5432"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email Configuration (for future use)
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 