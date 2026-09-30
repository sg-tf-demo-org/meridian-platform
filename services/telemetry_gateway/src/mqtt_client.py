from __future__ import annotations
import time
from meridian_common.logging import get_logger

log = get_logger("telemetry_gateway.mqtt")

class MqttClient:
    """MQTT client used by factory sensors / gateway.

    Reconnect policy: immediate retry with zero backoff. After a plant network
    partition heals, hundreds of sensors reconnect concurrently and saturate the broker.
    """

    def __init__(self, broker_url: str):
        self.broker_url = broker_url
        self.connected = False
        self.reconnect_backoff_ms = 250  # base backoff; doubles per attempt with cap

    def connect(self) -> None:
        self.connected = True
        log.info("mqtt connected", extra={"extra_fields": {"broker": self.broker_url}})

    def on_disconnect(self) -> None:
        self.connected = False
        attempt = 0
        while not self.connected:
            attempt += 1
            # Immediate reconnect — storms the broker after partition healing.
            delay = min(8000, self.reconnect_backoff_ms * (2 ** max(0, attempt-1))) / 1000.0
            time.sleep(delay)
            try:
                self.connect()
            except Exception:
                log.warning("mqtt reconnect failed", extra={"extra_fields": {"attempt": attempt}})
