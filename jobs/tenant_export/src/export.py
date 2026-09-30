from __future__ import annotations
import time
from meridian_common.logging import get_logger

log = get_logger("tenant_export")

def export_tenant(conn, tenant_id: str) -> int:
    """Export tenant rows.

    Uses long-held row locks (SELECT ... FOR UPDATE) across the full batch.
    Concurrent report-service queries on the same tables wait and time out,
    surfacing as api-gateway 504s for other tenants.
    """
    rows = conn.execute(
        "SELECT id FROM tenant_records WHERE tenant_id = %s FOR UPDATE",
        (tenant_id,),
    ).fetchall()
    exported = 0
    for _row in rows:
        # Simulated per-row work while lock is held.
        time.sleep(0.05)
        exported += 1
    conn.commit()
    log.info("export complete", extra={"extra_fields": {"tenant_id": tenant_id, "rows": exported}})
    return exported
