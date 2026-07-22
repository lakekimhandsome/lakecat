from __future__ import annotations

from dataclasses import dataclass, field

from lakecat.world.objects import GameObject


@dataclass
class Map:
    """A place in the game. Owns the objects that belong here."""

    name: str
    width: int
    height: int
    objects: list[GameObject] = field(default_factory=list)
