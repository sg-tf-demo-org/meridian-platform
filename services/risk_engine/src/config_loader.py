from __future__ import annotations
import os
from pathlib import Path
import yaml

DEFAULT = Path(__file__).resolve().parents[3] / "configs" / "risk" / "cfg-8842.yaml"

def load_risk_config() -> dict:
    path = Path(os.environ.get("MERIDIAN_RISK_CONFIG", str(DEFAULT)))
    with path.open() as f:
        return yaml.safe_load(f)
