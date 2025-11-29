/**
 * Performance-optimized API hook with caching and error handling
 * Senior Engineer Principle: Minimize network requests, cache aggressively
 */
import { useState, useEffect, useCallback, useRef } from 'react';

// Simple client-side cache
const apiCache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

export function useApi(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef(null);
  
  const { 
    cache = true, 
    cacheTTL = CACHE_TTL,
    dependencies = [],
    immediate = true 
  } = options;

  const fetchData = useCallback(async () => {
    // Cancel previous request if still pending
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Check cache first
    if (cache) {
      const cacheKey = url;
      const cached = apiCache.get(cacheKey);
      if (cached && Date.now() - cached.timestamp < cacheTTL) {
        setData(cached.data);
        setLoading(false);
        return cached.data;
      }
    }

    setLoading(true);
    setError(null);
    
    // Create new abort controller
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`http://localhost:8000${url}`, {
        signal: abortControllerRef.current.signal,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Cache successful response
      if (cache) {
        apiCache.set(url, {
          data: result,
          timestamp: Date.now()
        });
      }

      setData(result);
      return result;
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err.message);
        console.error('API Error:', err);
      }
    } finally {
      setLoading(false);
    }
  }, [url, cache, cacheTTL]);

  // Auto-fetch on mount and dependency changes
  useEffect(() => {
    if (immediate) {
      fetchData();
    }
    
    // Cleanup on unmount
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [fetchData, immediate, ...dependencies]);

  // Manual refresh function
  const refresh = useCallback(() => {
    // Clear cache for this URL
    if (cache) {
      apiCache.delete(url);
    }
    return fetchData();
  }, [fetchData, cache, url]);

  return { data, loading, error, refresh };
}

// Specialized hooks for common endpoints
export function useKPIs(days = 30) {
  return useApi(`/api/v1/dashboard/kpis?days=${days}`, {
    cache: true,
    cacheTTL: 3 * 60 * 1000, // 3 minutes for KPIs
    dependencies: [days]
  });
}

export function useRevenueTrend(days = 30) {
  return useApi(`/api/v1/dashboard/revenue-trend?days=${days}`, {
    cache: true,
    cacheTTL: 5 * 60 * 1000, // 5 minutes for trends
    dependencies: [days]
  });
}