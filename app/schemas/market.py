"""
Market data schemas.
"""

from pydantic import BaseModel, Field
from typing import Literal


class OHLCVParams(BaseModel):
    """Parameters for OHLCV data requests."""
    start: str = Field(default="", description="Start date YYYY-MM-DD. If empty, uses length.")
    end: str = Field(default="", description="End date YYYY-MM-DD. If empty, uses today.")
    interval: str = Field(default="1D", description="Interval: 1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M")
    length: int = Field(default=90, ge=1, le=5000, description="Number of bars if start/end not provided")


class QuoteParams(BaseModel):
    """Parameters for real-time quote requests."""
    symbols: list[str] = Field(default=[], description="List of symbols. Empty = all.")
