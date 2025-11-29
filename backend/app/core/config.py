from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./analytics.db"
    
    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Retail Analytics API"
    
    # Google Sheets (optional for MVP)
    google_credentials_file: Optional[str] = None
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-only-for-local-development")
    
    # CORS Origins - Environment specific
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # Production origins (override via environment)
    @property
    def allowed_origins(self) -> List[str]:
        env_origins = os.getenv("CORS_ORIGINS")
        if env_origins:
            return [origin.strip() for origin in env_origins.split(",")]
        return self.cors_origins
    
    class Config:
        env_file = ".env"


settings = Settings()