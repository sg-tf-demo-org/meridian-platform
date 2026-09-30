from __future__ import annotations
from fastapi import FastAPI
from prometheus_client import make_asgi_app, Gauge
from .mqtt_client import MqttClient

app = FastAPI(title="Meridian Telemetry Gateway")
app.mount("/metrics", make_asgi_app())
BROKER_ERRORS = Gauge("meridian_mqtt_broker_error_ratio", "Broker error ratio")
CPU_THROTTLE = Gauge("meridian_mqtt_broker_cpu_throttle", "Broker CPU throttle ratio")
CLIENTS = Gauge("meridian_mqtt_connected_clients", "Connected MQTT clients")
client = MqttClient("mqtt://mqtt-broker:1883")

@app.on_event("startup")
def startup():
    client.connect()

@app.get("/healthz")
def healthz():
    return {"ok": True, "connected": client.connected, "backoff_ms": client.reconnect_backoff_ms}

@app.post("/v1/simulate_reconnect_storm")
def simulate(n: int = 200):
    CLIENTS.set(n)
    BROKER_ERRORS.set(0.0396)
    CPU_THROTTLE.set(0.55)
    return {"clients": n, "error_ratio": 0.0396, "cpu_throttle": 0.55}
