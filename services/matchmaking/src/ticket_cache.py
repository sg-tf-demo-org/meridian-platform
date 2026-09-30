from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class TicketCache:
    """In-memory ticket cache with no size cap — grows without bound under patch-day load."""
    _tickets: dict[str, dict] = field(default_factory=dict)

    def put(self, ticket_id: str, payload: dict) -> None:
        self._tickets[ticket_id] = payload

    def size(self) -> int:
        return len(self._tickets)

    def approx_bytes(self) -> int:
        # Rough stand-in for working set growth observed in production (~441MB).
        return self.size() * 2048
