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


_current_key_index: int = 0


def init_vnstock():
    """Initialize vnstock instances. Call once at startup."""
    global _market, _reference, _fundamental, _retail, _current_key_index
    settings = get_settings()

    # Register first API key if provided
    keys = settings.vnstock_api_keys
    if keys:
        try:
            from vnstock import register_user
            register_user(api_key=keys[0])
            _current_key_index = 0
            logger.info(f"Vnstock API key index 0 registered successfully (starts with {keys[0][:12]}...)")
        except Exception as e:
            logger.warning(f"Failed to register first vnstock API key: {e}")

    _market = Market()
    _reference = Reference()
    _fundamental = Fundamental()
    _retail = Retail()
    logger.info("Vnstock instances initialized (Unified UI v4+)")


def rotate_vnstock_key() -> bool:
    """Rotate to the next configured vnstock API key."""
    global _current_key_index
    settings = get_settings()
    keys = settings.vnstock_api_keys
    if not keys or len(keys) <= 1:
        logger.info("No alternative API keys configured for rotation")
        return False

    _current_key_index = (_current_key_index + 1) % len(keys)
    new_key = keys[_current_key_index]
    try:
        from vnstock import register_user
        register_user(api_key=new_key)
        logger.info(f"Successfully rotated to vnstock API key index {_current_key_index} (starts with {new_key[:12]}...)")
        return True
    except Exception as e:
        logger.error(f"Failed to register rotated vnstock API key index {_current_key_index}: {e}")
        return False


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
