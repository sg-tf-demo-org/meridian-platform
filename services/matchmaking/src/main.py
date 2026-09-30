from __future__ import annotations
from fastapi import FastAPI
from prometheus_client import make_asgi_app
from meridian_common import metrics as m
from .ticket_cache import TicketCache

app = FastAPI(title="Meridian Matchmaking")
app.mount("/metrics", make_asgi_app())
cache = TicketCache()

@app.get("/healthz")
def healthz():
    return {"ok": True, "tickets": cache.size()}

@app.post("/v1/ticket")
def ticket(ticket_id: str, region: str = "na"):
    cache.put(ticket_id, {"region": region, "blob": "x" * 1024})
    m.MEMORY_BYTES.labels("matchmaking").set(cache.approx_bytes())
    if cache.approx_bytes() > 400_000_000:
        m.ERRORS.labels("matchmaking", "ticket").inc()
        return {"status": "degraded", "tickets": cache.size()}
    return {"status": "ok", "tickets": cache.size()}
