from __future__ import annotations
from fastapi import FastAPI
from prometheus_client import make_asgi_app, Counter, Gauge
from .config_loader import load_edge_config

app = FastAPI(title="Meridian Edge Router")
app.mount("/metrics", make_asgi_app())
CACHE_HIT = Counter("meridian_edge_cache_hits_total", "Edge cache hits")
CACHE_MISS = Counter("meridian_edge_cache_misses_total", "Edge cache misses")
ORIGIN_QPS = Gauge("meridian_origin_packager_qps", "Origin packager QPS")
SEGMENT_5XX = Counter("meridian_segment_5xx_total", "Segment 5xx")
CFG = load_edge_config()

def cache_key(title_id: str, bitrate: str, region: str, quality_tier: str) -> str:
    fields = CFG["segment_cache"]["cache_key_fields"]
    parts = {
        "title_id": title_id,
        "bitrate": bitrate,
        "region": region,
        "quality_tier": quality_tier,
    }
    return "|".join(parts[f] for f in fields if f in parts)

@app.get("/healthz")
def healthz():
    return {"ok": True, "config": CFG["version"], "fields": CFG["segment_cache"]["cache_key_fields"]}

@app.get("/v1/segment")
def segment(title_id: str, bitrate: str, region: str, quality_tier: str = "hd"):
    key = cache_key(title_id, bitrate, region, quality_tier)
    # Without quality_tier in the key, HD/SD collide → origin fan-out under game-day traffic.
    if "quality_tier" not in CFG["segment_cache"]["cache_key_fields"]:
        CACHE_MISS.inc()
        ORIGIN_QPS.inc()
        SEGMENT_5XX.inc()
        return {"key": key, "status": "origin", "code": 502}
    CACHE_HIT.inc()
    return {"key": key, "status": "hit", "code": 200}
