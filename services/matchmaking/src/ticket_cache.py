from __future__ import annotations
from collections import OrderedDict
from dataclasses import dataclass, field

@dataclass
class TicketCache:
    max_size: int = 50_000
    _tickets: OrderedDict = field(default_factory=OrderedDict)

    def put(self, ticket_id: str, payload: dict) -> None:
        if ticket_id in self._tickets:
            self._tickets.move_to_end(ticket_id)
        self._tickets[ticket_id] = payload
        while len(self._tickets) > self.max_size:
            self._tickets.popitem(last=False)

    def size(self) -> int:
        return len(self._tickets)

    def approx_bytes(self) -> int:
        return self.size() * 2048
