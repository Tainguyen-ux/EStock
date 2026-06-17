"""
In-memory TTL cache utilities using cachetools.
Provides simple caching to respect vnstock rate limits.
"""

from cachetools import TTLCache
from functools import wraps
import hashlib
import json
from typing import Any


# Cache stores for different data categories
_caches: dict[str, TTLCache] = {}


def get_cache(category: str, ttl: int, maxsize: int = 256) -> TTLCache:
    """Get or create a TTL cache for the given category."""
    if category not in _caches:
        _caches[category] = TTLCache(maxsize=maxsize, ttl=ttl)
    return _caches[category]


def make_cache_key(*args, **kwargs) -> str:
    """Create a deterministic cache key from arguments."""
    key_parts = [str(a) for a in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    raw_key = "|".join(key_parts)
    return hashlib.md5(raw_key.encode()).hexdigest()


def cached(category: str, ttl: int, maxsize: int = 256):
    """
    Decorator for caching function results with TTL.

    Args:
        category: Cache category name (e.g., 'quote', 'ohlcv')
        ttl: Time-to-live in seconds
        maxsize: Maximum number of cached items
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache = get_cache(category, ttl, maxsize)
            key = make_cache_key(func.__name__, *args, **kwargs)
            if key in cache:
                return cache[key]
            result = await func(*args, **kwargs)
            cache[key] = result
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache = get_cache(category, ttl, maxsize)
            key = make_cache_key(func.__name__, *args, **kwargs)
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            return result

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def clear_cache(category: str | None = None):
    """Clear cache for a specific category or all caches."""
    if category:
        if category in _caches:
            _caches[category].clear()
    else:
        for cache in _caches.values():
            cache.clear()


def cache_stats() -> dict[str, Any]:
    """Get cache statistics for monitoring."""
    stats = {}
    for name, cache in _caches.items():
        stats[name] = {
            "current_size": len(cache),
            "max_size": cache.maxsize,
            "ttl": cache.timer() if hasattr(cache, 'timer') else None,
        }
    return stats
