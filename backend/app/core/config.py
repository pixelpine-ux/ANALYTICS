from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./analytics.db"
    
    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Retail Analytics API"
    
    # Google Sheets (optional for MVP)
    google_credentials_file: Optional[str] = None
    
    # Security
    secret_key: str = "dev-secret-change-in-production"
    
    class Config:
        env_file = ".env"


settings = Settings()