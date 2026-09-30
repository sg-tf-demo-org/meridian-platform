from __future__ import annotations
import time
from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app
from sqlalchemy import text
from sqlalchemy.exc import TimeoutError as SATimeout
from meridian_common import metrics as m
from meridian_common.logging import get_logger
from .db import engine, POOL_SIZE

log = get_logger("appointments")
app = FastAPI(title="Meridian Appointments")
app.mount("/metrics", make_asgi_app())
m.POOL_MAX.labels("appointments").set(POOL_SIZE)

@app.get("/healthz")
def healthz():
    return {"ok": True, "pool_size": POOL_SIZE}

@app.post("/v1/book")
def book(slot_id: str = "am-0900"):
    m.POOL_ACTIVE.labels("appointments").inc()
    start = time.perf_counter()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        m.REQUESTS.labels("appointments", "book", "200").inc()
        return {"slot_id": slot_id, "status": "booked"}
    except SATimeout as exc:
        m.ERRORS.labels("appointments", "book").inc()
        m.REQUESTS.labels("appointments", "book", "503").inc()
        msg = f"Connection is not available, request timed out after {int(engine.pool.timeout()*1000)}ms"
        log.error(msg)
        raise HTTPException(status_code=503, detail=msg) from exc
    finally:
        m.POOL_ACTIVE.labels("appointments").dec()
        m.LATENCY.labels("appointments", "book").observe(time.perf_counter() - start)
