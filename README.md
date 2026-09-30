# Meridian Platform

Internal monorepo for Meridian commerce, risk, clinical scheduling, factory telemetry,
travel quotes, media edge delivery, matchmaking, and tenant reporting.

## Layout

| Path | Service |
|------|---------|
| `services/checkout` | Checkout orchestration and card-network auth |
| `services/risk_engine` | Authorization risk / velocity checks |
| `services/appointments` | Clinic appointment booking |
| `services/telemetry_gateway` | Factory MQTT telemetry ingress |
| `services/travel_quotes` | Fare quote + revalidation |
| `services/edge_router` | Segment cache / origin routing |
| `services/matchmaking` | Lobby ticket matchmaking |
| `services/reporting` | Multi-tenant report API |
| `jobs/tenant_export` | Batch tenant data export |
| `configs/risk` | Versioned risk engine configs |
| `configs/edge` | Versioned edge-router configs |

## Local run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn services.checkout.src.main:app --reload --port 8081
```

Compose stack (Postgres + services):

```bash
docker compose -f deploy/compose/docker-compose.yml up --build
```

## Config versions

Risk engine loads `MERIDIAN_RISK_CONFIG` (default `configs/risk/cfg-8842.yaml`).
Edge router loads `MERIDIAN_EDGE_CONFIG` (default `configs/edge/cfg-7701.yaml`).
