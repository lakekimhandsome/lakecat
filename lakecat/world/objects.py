from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    """World-space coordinates only. Never store screen coordinates here."""

    x: int
    y: int


@dataclass
class GameObject:
    """Something that exists on a Map, in world coordinates only."""

    name: str
    world_x: int
    world_y: int
    width: int
    height: int
    sprite: list[str]
    solid: bool = True

    @classmethod
    def from_sprite(
        cls,
        name: str,
        world_x: int,
        world_y: int,
        sprite: list[str],
        *,
        solid: bool = True,
    ) -> GameObject:
        height = len(sprite)
        width = max((len(line) for line in sprite), default=0)
        return cls(
            name=name,
            world_x=world_x,
            world_y=world_y,
            width=width,
            height=height,
            sprite=sprite,
            solid=solid,
        )
