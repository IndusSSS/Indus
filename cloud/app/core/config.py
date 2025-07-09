# app/core/config.py
"""
Application configuration settings.

• Loads from environment variables with sensible defaults.
• Validates required settings on startup.
• Provides type-safe access to all config values.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ─────────────────── API Settings ──────────────────── #
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # ─────────────────── Database ──────────────────────── #
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/cloud"
    DATABASE_ECHO: bool = False
    
    # ─────────────────── Security ──────────────────────── #
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ─────────────────── Redis ─────────────────────────── #
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ─────────────────── MQTT ──────────────────────────── #
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None


# Global settings instance
settings = Settings()