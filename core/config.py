"""
SORT - Software Operation and Resource Team
Core Configuration Module
"""

from typing import Dict, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Project Meta
    PROJECT_NAME: str = "SORT"
    VERSION: str = "0.1.0"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/sort_db"
    
    # Model Configuration
    CTO_MODEL: str = "mistralai/Mistral-7B-v0.1"
    CODING_MODEL: str = "Qwen/Qwen-7B"
    TESTING_MODEL: str = "minicpm/MiniCPM-2B-dpo"
    DOCUMENTATION_MODEL: str = "google/gemini-pro"
    FINANCE_MODEL: str = "ProsusAI/finbert"
    
    # API Keys and Integration Settings
    GITHUB_TOKEN: Optional[str] = None
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Agent Communication
    AGENT_COMMUNICATION_PROTOCOL: str = "async_messaging"
    MAX_RETRY_ATTEMPTS: int = 3
    TIMEOUT_SECONDS: int = 30
    
    # Health Checking
    HEALTH_CHECK_INTERVAL: int = 60  # seconds
    SELF_HEALING_ENABLED: bool = True
    
    # Feature Flags
    ENABLE_PROMPT_OPTIMIZATION: bool = True
    ENABLE_SELF_HEALING: bool = True
    ENABLE_MONITORING: bool = True
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
