"""
Stock screener filter schemas.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FAScreenerParams(BaseModel):
    """Fundamental Analysis screener filters."""
    exchange: str = Field(default="", description="Filter by exchange: HOSE, HNX, UPCOM. Empty = all.")
    group: str = Field(default="", description="Filter by group: VN30, HNX30, etc. Empty = all.")

    # Valuation filters
    pe_max: float | None = Field(default=None, description="Maximum P/E ratio")
    pe_min: float | None = Field(default=None, description="Minimum P/E ratio")
    pb_max: float | None = Field(default=None, description="Maximum P/B ratio")
    pb_min: float | None = Field(default=None, description="Minimum P/B ratio")

    # Profitability filters
    roe_min: float | None = Field(default=None, description="Minimum ROE (%)")
    roa_min: float | None = Field(default=None, description="Minimum ROA (%)")
    gross_margin_min: float | None = Field(default=None, description="Minimum gross profit margin (%)")
    net_margin_min: float | None = Field(default=None, description="Minimum net profit margin (%)")

    # Leverage filters
    debt_equity_max: float | None = Field(default=None, description="Maximum Debt/Equity ratio")

    # Growth filters
    revenue_growth_min: float | None = Field(default=None, description="Minimum revenue growth YoY (%)")
    profit_growth_min: float | None = Field(default=None, description="Minimum profit growth YoY (%)")

    # Pagination
    limit: int = Field(default=50, ge=1, le=500, description="Max results")


class TAScreenerParams(BaseModel):
    """Technical Analysis screener filters."""
    exchange: str = Field(default="", description="Filter by exchange: HOSE, HNX, UPCOM. Empty = all.")
    group: str = Field(default="", description="Filter by group: VN30, HNX30, etc. Empty = all.")
    symbols: list[str] = Field(default=[], description="Specific symbols to screen. Empty = use group/exchange.")

    # Moving Average filters
    ma_cross_up: bool = Field(default=False, description="Price crossed above SMA20")
    ma_cross_down: bool = Field(default=False, description="Price crossed below SMA20")
    above_ma20: bool | None = Field(default=None, description="Price above SMA20")
    above_ma50: bool | None = Field(default=None, description="Price above SMA50")

    # RSI filters
    rsi_oversold: bool = Field(default=False, description="RSI < 30 (oversold)")
    rsi_overbought: bool = Field(default=False, description="RSI > 70 (overbought)")
    rsi_min: float | None = Field(default=None, description="Minimum RSI value")
    rsi_max: float | None = Field(default=None, description="Maximum RSI value")

    # Volume filters
    volume_spike: bool = Field(default=False, description="Volume > 2x average 20 sessions")
    volume_spike_ratio: float = Field(default=2.0, ge=1.0, description="Volume spike multiplier vs 20-day avg")

    # MACD filters
    macd_cross_up: bool = Field(default=False, description="MACD crossed above signal line")

    # Period for calculation
    lookback_days: int = Field(default=60, ge=20, le=365, description="Lookback period for TA calculation")

    # Pagination
    limit: int = Field(default=50, ge=1, le=500, description="Max results")


class CompareParams(BaseModel):
    """Parameters for comparing multiple stocks."""
    symbols: list[str] = Field(..., min_length=2, max_length=20, description="List of symbols to compare")
    include_price: bool = Field(default=True, description="Include price comparison")
    include_fundamental: bool = Field(default=True, description="Include fundamental comparison")
    period: str = Field(default="90", description="Price history period in days")
