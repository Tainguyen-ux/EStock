"""
Shared dependencies and vnstock singleton instances.
Initializes Market, Reference, Fundamental, Retail once and reuses.
"""

from vnstock import Market, Reference, Fundamental, Retail
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# Vnstock singleton instances (Unified UI v4+)
# ──────────────────────────────────────────────────────────────
_market: Market | None = None
_reference: Reference | None = None
_fundamental: Fundamental | None = None
_retail: Retail | None = None


def init_vnstock():
    """Initialize vnstock instances. Call once at startup."""
    global _market, _reference, _fundamental, _retail
    settings = get_settings()

    # Register API key if provided
    if settings.VNSTOCK_API_KEY:
        try:
            from vnstock import register_user
            register_user(api_key=settings.VNSTOCK_API_KEY)
            logger.info("Vnstock API key registered successfully")
        except Exception as e:
            logger.warning(f"Failed to register vnstock API key: {e}")

    _market = Market()
    _reference = Reference()
    _fundamental = Fundamental()
    _retail = Retail()
    logger.info("Vnstock instances initialized (Unified UI v4+)")


def get_market() -> Market:
    """Get Market instance for price/trading data."""
    if _market is None:
        init_vnstock()
    return _market


def get_reference() -> Reference:
    """Get Reference instance for listing/company data."""
    if _reference is None:
        init_vnstock()
    return _reference


def get_fundamental() -> Fundamental:
    """Get Fundamental instance for financial reports."""
    if _fundamental is None:
        init_vnstock()
    return _fundamental


def get_retail() -> Retail:
    """Get Retail instance for gold/exchange rate data."""
    if _retail is None:
        init_vnstock()
    return _retail
