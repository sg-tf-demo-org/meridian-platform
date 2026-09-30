from __future__ import annotations
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app, Counter
from .fare_cache import FareCache, FareEntry

app = FastAPI(title="Meridian Travel Quotes")
app.mount("/metrics", make_asgi_app())
REVAL_FAIL = Counter("meridian_fare_revalidation_failures_total", "Revalidation failures")
cache = FareCache()
# Seed a stale fare as if AeroFare feed degraded.
cache.put(FareEntry(
    fare_id="AF-1001",
    amount=412.50,
    as_of=datetime.now(timezone.utc) - timedelta(hours=5, minutes=40),
    generation="stale-gen-77",
))

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/v1/revalidate")
def revalidate(fare_id: str = "AF-1001", live_amount: float = 489.00):
    entry = cache.get(fare_id)
    if entry is None:
        raise HTTPException(404, "fare not found")
    # Missing freshness gate: compare live quote to cached amount regardless of as_of.
    if abs(entry.amount - live_amount) > 1.0:
        REVAL_FAIL.inc()
        raise HTTPException(
            status_code=409,
            detail=f"revalidation failed fare_id={fare_id} cache_gen={entry.generation} as_of={entry.as_of.isoformat()}",
        )
    return {"fare_id": fare_id, "status": "ok"}
