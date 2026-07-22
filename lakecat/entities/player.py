from __future__ import annotations

from dataclasses import dataclass

from lakecat.assets.sprites import PLAYER_GLYPH
from lakecat.world.objects import Position


@dataclass
class Player:
    """Player state only. Collision decisions live in World / collision."""

    position: Position
    glyph: str = PLAYER_GLYPH
    width: int = 2
    height: int = 1
    move_speed_x: int = 2
    move_speed_y: int = 1

    def proposed_position(self, dx: int, dy: int) -> Position:
        """Where a move command would place the player (world space)."""
        return Position(
            x=self.position.x + dx * self.move_speed_x,
            y=self.position.y + dy * self.move_speed_y,
        )

    def place_at(self, x: int, y: int) -> None:
        self.position.x = x
        self.position.y = y
