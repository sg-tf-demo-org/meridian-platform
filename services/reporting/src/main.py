from __future__ import annotations
from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app
from meridian_common.logging import get_logger

log = get_logger("reporting")
app = FastAPI(title="Meridian Reporting")
app.mount("/metrics", make_asgi_app())

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/v1/reports/{tenant_id}")
def report(tenant_id: str):
    # Shared-DB path; fails with gateway 504 when tenant_export holds row locks.
    raise HTTPException(status_code=504, detail=f"report-service timed out for tenant={tenant_id}")
