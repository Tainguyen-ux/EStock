"""
Application configuration using pydantic-settings.
Loads from .env file or environment variables.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: str = "*"

    # Vnstock
    VNSTOCK_API_KEY: str = ""

    # Cache TTL (seconds)
    CACHE_TTL_QUOTE: int = 30        # Real-time quote: 30s
    CACHE_TTL_OHLCV: int = 300       # Historical OHLCV: 5 min
    CACHE_TTL_REFERENCE: int = 3600  # Reference data: 1 hour
    CACHE_TTL_FUNDAMENTAL: int = 3600  # Financial reports: 1 hour
    CACHE_TTL_RETAIL: int = 600      # Gold/FX rates: 10 min

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse CORS origins string into list."""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def vnstock_api_keys(self) -> list[str]:
        """Parse VNSTOCK_API_KEY string into a list of keys."""
        if not self.VNSTOCK_API_KEY:
            return []
        return [k.strip() for k in self.VNSTOCK_API_KEY.split(",") if k.strip()]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
