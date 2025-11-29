"""
Performance Caching Layer
Senior Engineer Principle: Cache expensive operations, not cheap ones
"""
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import json
import hashlib
from functools import wraps

class MemoryCache:
    """
    Simple in-memory cache with TTL (Time To Live)
    Production: Replace with Redis for multi-instance deployments
    """
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def _generate_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key from parameters"""
        # Sort kwargs for consistent keys
        sorted_params = sorted(kwargs.items())
        param_string = json.dumps(sorted_params, sort_keys=True)
        hash_key = hashlib.md5(param_string.encode()).hexdigest()[:8]
        return f"{prefix}:{hash_key}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if datetime.utcnow() > entry['expires_at']:
            del self._cache[key]
            return None
        
        return entry['value']
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Set value in cache with TTL"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        self._cache[key] = {
            'value': value,
            'expires_at': expires_at
        }
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
    
    def stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            'total_keys': len(self._cache),
            'expired_keys': sum(1 for entry in self._cache.values() 
                              if datetime.utcnow() > entry['expires_at'])
        }

# Global cache instance
cache = MemoryCache()

def cached(prefix: str, ttl_seconds: int = 300):
    """
    Decorator for caching function results
    
    Usage:
    @cached("kpi_summary", ttl_seconds=600)  # 10 minutes
    def calculate_expensive_kpis(days: int):
        # expensive calculation
        return result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function parameters
            cache_key = cache._generate_key(prefix, args=args, kwargs=kwargs)
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Calculate and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        
        return wrapper
    return decorator

def cache_invalidate(prefix: str, **kwargs):
    """Invalidate specific cache entries"""
    key = cache._generate_key(prefix, **kwargs)
    if key in cache._cache:
        del cache._cache[key]