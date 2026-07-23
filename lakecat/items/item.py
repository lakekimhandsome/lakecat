from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """Catalog entry for something that can sit in an Inventory."""

    id: str
    name: str
    icon: str
    max_stack: int = 99
