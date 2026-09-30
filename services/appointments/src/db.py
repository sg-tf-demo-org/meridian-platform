from __future__ import annotations
import os
from sqlalchemy import create_engine

# Pool sized for overnight quiet hours — too small for 09:00 clinic open surge.
POOL_SIZE = int(os.environ.get("APPOINTMENTS_POOL_SIZE", "10"))
POOL_TIMEOUT = int(os.environ.get("APPOINTMENTS_POOL_TIMEOUT", "30"))
DATABASE_URL = os.environ.get(
    "APPOINTMENTS_DATABASE_URL",
    "postgresql+psycopg://meridian:meridian@localhost:5432/appointments",
)

engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=0,
    pool_timeout=POOL_TIMEOUT,
)
