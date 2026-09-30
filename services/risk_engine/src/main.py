from __future__ import annotations
from fastapi import FastAPI
from prometheus_client import make_asgi_app, Gauge
from meridian_common.logging import get_logger
from .config_loader import load_risk_config

log = get_logger("risk_engine")
app = FastAPI(title="Meridian Risk Engine")
app.mount("/metrics", make_asgi_app())
THRESHOLD = Gauge("meridian_risk_velocity_check_47", "Velocity check threshold")
CFG = load_risk_config()
THRESHOLD.set(float(CFG["thresholds"]["velocity_check_47"]))
log.info("loaded risk config", extra={"extra_fields": {
    "risk_config_version": CFG["version"],
    "velocity_check_47": CFG["thresholds"]["velocity_check_47"],
    "engine_image": CFG.get("engine_image"),
}})

@app.get("/healthz")
def healthz():
    return {"ok": True, "config": CFG["version"]}

@app.post("/v1/authorize")
def authorize(score: float = 0.2):
    thr = float(CFG["thresholds"]["velocity_check_47"])
    declined = score >= thr
    # With thr=0.10, legitimate scores 0.05-0.30 are mostly declined.
    return {
        "decision": "decline" if declined else "approve",
        "score": score,
        "velocity_check_47": thr,
        "risk_config_version": CFG["version"],
    }
