# Tests for response cache

import pytest
from utils.cache import ResponseCache


class TestResponseCache:
    def test_cache_set_and_get(self):
        """Test basic cache set and get"""
        cache = ResponseCache()
        cache.set("key1", value="value1")
        result = cache.get("key1")
        assert result == "value1"

    def test_cache_miss(self):
        """Test cache miss returns None"""
        cache = ResponseCache()
        result = cache.get("nonexistent")
        assert result is None

    def test_cache_hit_rate(self):
        """Test cache hit rate calculation"""
        cache = ResponseCache()
        cache.set("key1", value="value1")
        cache.get("key1")
        cache.get("key1")

        stats = cache.get_stats()
        assert stats["hits"] == 2
        assert stats["misses"] == 0
        assert stats["hit_rate"] == 1.0

    def test_cache_eviction(self):
        """Test cache eviction at max size"""
        cache = ResponseCache(max_size=3)
        cache.set("key1", value="value1")
        cache.set("key2", value="value2")
        cache.set("key3", value="value3")
        cache.set("key4", value="value4")  # Should evict key1

        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
        assert cache.get("key4") == "value4"

    def test_cache_clear(self):
        """Test cache clear"""
        cache = ResponseCache()
        cache.set("key1", value="value1")
        cache.clear()

        assert cache.get("key1") is None
        # Note: get() after clear() will increment misses, so we check cache is empty
        assert cache.get_stats()["cache_size"] == 0

    def test_cache_with_different_inputs(self):
        """Test cache with different input combinations"""
        cache = ResponseCache()

        # Same inputs should hit
        cache.set("test", arg1="a", arg2="b", value="same")
        result1 = cache.get("test", arg1="a", arg2="b")
        assert result1 == "same"

        # Different inputs should miss
        result2 = cache.get("test", arg1="a", arg2="c")
        assert result2 is None
