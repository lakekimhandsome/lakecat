from __future__ import annotations

from dataclasses import dataclass

from lakecat.world.objects import Position


@dataclass
class NPC:
    """Stub for future dialogue / quests. World coordinates only."""

    name: str
    position: Position
    glyph: str = "?"
