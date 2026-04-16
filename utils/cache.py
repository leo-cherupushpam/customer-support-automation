# Response cache for LLM optimization

import hashlib
import json
from typing import Optional, Dict, Any


class ResponseCache:
    """LRU cache for LLM responses to reduce costs"""

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, Any] = {}
        self.hits = 0
        self.misses = 0

    def _hash_input(self, *args, **kwargs) -> str:
        """Create hash key from input arguments"""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, *args, **kwargs) -> Optional[Any]:
        """Get cached response"""
        key = self._hash_input(*args, **kwargs)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        return None

    def set(self, *args, **kwargs) -> None:
        """Cache a response"""
        value = kwargs.pop("value", None)
        key = self._hash_input(*args, **kwargs)

        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size:
            # Remove first item (oldest in dict insertion order)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[key] = value

    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / max(total, 1)

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache),
            "max_size": self.max_size,
        }

    def clear(self) -> None:
        """Clear the cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def _hash_input(self, *args, **kwargs) -> str:
        """Create hash key from input arguments"""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, *args, **kwargs) -> Optional[Any]:
        """Get cached response"""
        key = self._hash_input(*args, **kwargs)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        return None

    def set(self, *args, **kwargs) -> None:
        """Cache a response"""
        value = kwargs.pop("value", None)
        key = self._hash_input(*args, **kwargs)

        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size:
            # Remove first item (oldest in dict insertion order)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[key] = value

    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / max(total, 1)

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache),
            "max_size": self.max_size,
        }

    def clear(self) -> None:
        """Clear the cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def _hash_input(self, *args, **kwargs) -> str:
        """Create hash key from input arguments"""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, *args, **kwargs) -> Optional[Any]:
        """Get cached response"""
        key = self._hash_input(*args, **kwargs)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        return None

    def set(self, *args, **kwargs) -> None:
        """Cache a response"""
        value = kwargs.pop("value", None)
        key = self._hash_input(*args, **kwargs)

        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size:
            # Remove first item (oldest in dict insertion order)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        self.cache[key] = value

    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / max(total, 1)

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache),
            "max_size": self.max_size,
        }

    def clear(self) -> None:
        """Clear the cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
