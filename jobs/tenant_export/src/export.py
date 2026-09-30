from __future__ import annotations
import time
from meridian_common.logging import get_logger

log = get_logger("tenant_export")

CHUNK = 100

def export_tenant(conn, tenant_id: str) -> int:
    """Export tenant rows in short transactions with SKIP LOCKED."""
    exported = 0
    while True:
        rows = conn.execute(
            "SELECT id FROM tenant_records WHERE tenant_id = %s FOR UPDATE SKIP LOCKED LIMIT %s",
            (tenant_id, CHUNK),
        ).fetchall()
        if not rows:
            break
        for _row in rows:
            time.sleep(0.01)
            exported += 1
        conn.commit()
    log.info("export complete", extra={"extra_fields": {"tenant_id": tenant_id, "rows": exported}})
    return exported
