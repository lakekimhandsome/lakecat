from __future__ import annotations

from dataclasses import dataclass

from lakecat.world.objects import Position


@dataclass
class Camera:
    """Viewport origin in world space. Converts world → screen only."""

    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def resize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def center_on(self, target: Position) -> None:
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2

    def world_to_screen(self, world_x: int, world_y: int) -> tuple[int, int]:
        return world_x - self.x, world_y - self.y

    def screen_to_world(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        return screen_x + self.x, screen_y + self.y
