from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    service_name: str = "checkout"
    # Card-network auth must complete within this budget (ms).
    # Production p99 card-network RTT recently drifted above this value.
    auth_deadline_ms: int = 5000
    card_network_url: str = "http://payment-gateway:8080/card-network/auth"
    authorize_queue_depth_warn: int = 50

settings = Settings()
