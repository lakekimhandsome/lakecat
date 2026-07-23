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
    # Local offset + size used for collision when solid. None = full sprite bounds.
    hitbox: tuple[int, int, int, int] | None = None
    # If True, can draw over the player when the player is behind this object.
    occludes: bool = False

    def solid_bounds(self) -> tuple[int, int, int, int]:
        """World-space collision rectangle (x, y, width, height)."""
        if self.hitbox is None:
            return self.world_x, self.world_y, self.width, self.height
        ox, oy, w, h = self.hitbox
        return self.world_x + ox, self.world_y + oy, w, h

    @property
    def sort_y(self) -> int:
        """Foot row used for depth sorting."""
        return self.world_y + self.height - 1

    def covers_cell(self, world_x: int, world_y: int) -> bool:
        """True if this cell is inside the sprite silhouette (including hollow interiors).

        On each row, everything from the leftmost to rightmost non-space glyph counts,
        so canopy interiors hide the player even where the art is blank.
        """
        local_x = world_x - self.world_x
        local_y = world_y - self.world_y
        if local_y < 0 or local_y >= len(self.sprite):
            return False
        line = self.sprite[local_y]
        filled = [i for i, ch in enumerate(line) if ch != " "]
        if not filled:
            return False
        return filled[0] <= local_x <= filled[-1]

    @classmethod
    def from_sprite(
        cls,
        name: str,
        world_x: int,
        world_y: int,
        sprite: list[str],
        *,
        solid: bool = True,
        hitbox: tuple[int, int, int, int] | None = None,
        occludes: bool = False,
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
            hitbox=hitbox,
            occludes=occludes,
        )
