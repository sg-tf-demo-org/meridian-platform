from __future__ import annotations
import os
from pathlib import Path
import yaml

DEFAULT = Path(__file__).resolve().parents[3] / "configs" / "edge" / "cfg-7701.yaml"

def load_edge_config() -> dict:
    path = Path(os.environ.get("MERIDIAN_EDGE_CONFIG", str(DEFAULT)))
    with path.open() as f:
        return yaml.safe_load(f)
