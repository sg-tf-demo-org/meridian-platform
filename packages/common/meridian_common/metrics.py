from __future__ import annotations
from prometheus_client import Counter, Gauge, Histogram

REQUESTS = Counter("meridian_http_requests_total", "HTTP requests", ["service", "route", "code"])
ERRORS = Counter("meridian_http_errors_total", "HTTP errors", ["service", "route"])
LATENCY = Histogram("meridian_http_latency_seconds", "Latency", ["service", "route"])
BACKLOG = Gauge("meridian_authorize_backlog", "Authorize backlog depth", ["service"])
POOL_ACTIVE = Gauge("meridian_db_pool_active", "Active DB connections", ["service"])
POOL_MAX = Gauge("meridian_db_pool_max", "Max DB pool size", ["service"])
CACHE_HIT = Counter("meridian_cache_hits_total", "Cache hits", ["service"])
CACHE_MISS = Counter("meridian_cache_misses_total", "Cache misses", ["service"])
MEMORY_BYTES = Gauge("meridian_process_memory_bytes", "Approximate working set", ["service"])
LOCK_WAITS = Gauge("meridian_db_lock_waits", "DB lock waits", ["service"])
