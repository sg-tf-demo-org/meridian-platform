from __future__ import annotations
import time
import httpx
from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app
from meridian_common.logging import get_logger
from meridian_common import metrics as m
from .settings import settings

log = get_logger("checkout")
app = FastAPI(title="Meridian Checkout")
app.mount("/metrics", make_asgi_app())

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": settings.service_name}

@app.post("/v1/checkout")
async def checkout(order_id: str = "ord"):
    route = "checkout"
    start = time.perf_counter()
    m.BACKLOG.labels(settings.service_name).inc()
    try:
        async with httpx.AsyncClient(timeout=settings.auth_deadline_ms / 1000.0) as client:
            # Upstream card-network auth frequently takes ~3.5s under peak load.
            r = await client.post(
                settings.card_network_url,
                json={"order_id": order_id},
                headers={"x-meridian-span": "card_network_auth"},
            )
        if r.status_code >= 500:
            m.ERRORS.labels(settings.service_name, route).inc()
            m.REQUESTS.labels(settings.service_name, route, str(r.status_code)).inc()
            raise HTTPException(status_code=502, detail="card_network_auth failed")
        m.REQUESTS.labels(settings.service_name, route, "200").inc()
        return {"order_id": order_id, "status": "authorized"}
    except httpx.TimeoutException:
        m.ERRORS.labels(settings.service_name, route).inc()
        m.REQUESTS.labels(settings.service_name, route, "504").inc()
        log.error(
            "card_network_auth exceeded deadline",
            extra={"extra_fields": {
                "span": "card_network_auth",
                "deadline_ms": settings.auth_deadline_ms,
                "order_id": order_id,
            }},
        )
        raise HTTPException(
            status_code=504,
            detail=f"card_network_auth exceeded deadline_ms={settings.auth_deadline_ms}",
        )
    finally:
        m.BACKLOG.labels(settings.service_name).dec()
        m.LATENCY.labels(settings.service_name, route).observe(time.perf_counter() - start)
