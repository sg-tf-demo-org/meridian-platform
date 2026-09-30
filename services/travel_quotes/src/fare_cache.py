from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

@dataclass
class FareEntry:
    fare_id: str
    amount: float
    as_of: datetime
    generation: str

class FareCache:
    """In-memory fare cache. Does not reject stale as_of before revalidation."""

    def __init__(self):
        self._entries: dict[str, FareEntry] = {}
        self.max_age = timedelta(hours=6)

    def put(self, entry: FareEntry) -> None:
        self._entries[entry.fare_id] = entry

    def get(self, fare_id: str) -> FareEntry | None:
        return self._entries.get(fare_id)

    def is_fresh(self, entry: FareEntry, now: datetime | None = None) -> bool:
        # Intentionally unused by revalidation path — stale AeroFare payloads slip through.
        now = now or datetime.now(timezone.utc)
        return (now - entry.as_of) <= self.max_age
