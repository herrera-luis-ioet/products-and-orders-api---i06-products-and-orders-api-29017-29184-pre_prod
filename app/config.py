"""
Configuration settings for the application.

This module provides configuration management using Pydantic's BaseSettings
for environment variables and application settings.
"""

import os
from typing import Any, Dict, Optional

from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    
    Loads configuration from environment variables with fallback to default values.
    """
    # CORE SETTINGS
    ENV: str = Field(default="development", description="Environment (development, testing, production)")
    DEBUG: bool = Field(default=False, description="Debug mode")
    API_V1_STR: str = Field(default="/api/v1", description="API v1 prefix")
    PROJECT_NAME: str = Field(default="Product and Order Management API", description="Name of the project")
    
    # CORS SETTINGS
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = Field(
        default=["http://localhost:8000", "http://localhost:3000"],
        description="List of origins that can access the API"
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # DATABASE SETTINGS
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./products_orders.db",
        description="Database connection string"
    )
    
    # SECURITY SETTINGS
    SECRET_KEY: str = Field(
        default="supersecretkey",
        description="Secret key for JWT token generation and validation"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Minutes before an access token expires"
    )
    
    # APPLICATION SETTINGS
    PAGINATION_PAGE_SIZE: int = Field(
        default=10,
        description="Default number of items per page in paginated responses"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create a global settings instance
settings = Settings()