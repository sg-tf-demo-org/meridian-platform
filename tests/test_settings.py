from services.checkout.src.settings import settings
from services.risk_engine.src.config_loader import load_risk_config
from services.edge_router.src.config_loader import load_edge_config
from services.appointments.src.db import POOL_SIZE
from services.matchmaking.src.ticket_cache import TicketCache
from services.telemetry_gateway.src.mqtt_client import MqttClient

def test_checkout_deadline():
    assert settings.auth_deadline_ms == 3000

def test_risk_threshold():
    cfg = load_risk_config()
    assert cfg["thresholds"]["velocity_check_47"] == 0.10

def test_edge_cache_key_missing_quality_tier():
    cfg = load_edge_config()
    assert "quality_tier" not in cfg["segment_cache"]["cache_key_fields"]

def test_appointments_pool():
    assert POOL_SIZE == 10

def test_matchmaking_unbounded():
    c = TicketCache()
    for i in range(100):
        c.put(str(i), {"x": i})
    assert c.size() == 100

def test_mqtt_zero_backoff():
    assert MqttClient("mqtt://x").reconnect_backoff_ms == 0
