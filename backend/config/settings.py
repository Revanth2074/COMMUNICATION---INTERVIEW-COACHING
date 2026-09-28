"""
Application Settings for Interview Coach
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = Field(default="Interview Coach API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    
    # Database
    database_url: str = Field(default="sqlite:///interview_coach.db")
    
    # Authentication
    secret_key: str = Field(default="your-secret-key-here")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    
    # CORS
    cors_origins: list[str] = Field(default=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # File uploads
    upload_dir: str = "uploads"
    audio_upload_dir: str = "uploads/audio"
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    
    # API Keys (can be overridden by environment variables)
    omniroute_api_key: Optional[str] = Field(default=None)
    kiro_llm_api_key: Optional[str] = Field(default=None)
    
    # LLM Configuration
    default_llm_provider: str = "omniroute"
    default_model: str = "kiro"
    
    # Agent Configuration
    enable_multi_agent: bool = True
    agent_timeout: int = 60  # seconds
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = True


# Create settings instance
settings = Settings()
