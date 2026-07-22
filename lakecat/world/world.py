from __future__ import annotations

from dataclasses import dataclass

from lakecat.assets.sprites import TREE
from lakecat.engine.camera import Camera
from lakecat.entities.player import Player
from lakecat.world.collision import can_move_to
from lakecat.world.map import Map
from lakecat.world.objects import GameObject, Position


@dataclass
class World:
    """Single source of truth for game state."""

    map: Map
    player: Player
    camera: Camera

    def update(self) -> None:
        """Per-frame world simulation (AI, timers, etc.)."""
        pass

    def try_move_player(self, dx: int, dy: int) -> bool:
        """Apply a move request only if the destination is free of solid objects."""
        target = self.player.proposed_position(dx, dy)
        if not can_move_to(
            self.map,
            target.x,
            target.y,
            self.player.width,
            self.player.height,
        ):
            return False
        self.player.place_at(target.x, target.y)
        return True

    def sync_camera(self, screen_width: int, screen_height: int) -> None:
        """Keep the camera sized to the terminal and centered on the player."""
        self.camera.resize(screen_width, screen_height)
        self.camera.center_on(self.player.position)


def create_demo_world() -> World:
    """Initial playable world. Expand here as areas grow."""
    demo_map = Map(
        name="demo",
        width=200,
        height=200,
        objects=[
            GameObject.from_sprite(
                name="tree",
                world_x=40,
                world_y=8,
                sprite=TREE,
                solid=True,
            ),
        ],
    )
    return World(
        map=demo_map,
        player=Player(position=Position(x=0, y=0)),
        camera=Camera(),
    )
