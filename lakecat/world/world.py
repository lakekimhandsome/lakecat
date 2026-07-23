from __future__ import annotations

import random
from dataclasses import dataclass

from lakecat.assets.sprites import FLOWER, TREE, TREE_HITBOX
from lakecat.engine.camera import Camera
from lakecat.entities.player import Player
from lakecat.items.catalog import FISH, STONE, WOOD
from lakecat.world.collision import can_move_to, rects_overlap
from lakecat.world.map import Map
from lakecat.world.objects import GameObject, Position

_TREE_COUNT = 25
_FLOWER_COUNT = 40
_SPAWN_CLEARANCE = 6


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


def _sprite_size(sprite: list[str]) -> tuple[int, int]:
    height = len(sprite)
    width = max((len(line) for line in sprite), default=0)
    return width, height


def _overlaps_any(
    objects: list[GameObject],
    x: int,
    y: int,
    width: int,
    height: int,
) -> bool:
    for obj in objects:
        if rects_overlap(x, y, width, height, obj.world_x, obj.world_y, obj.width, obj.height):
            return True
    return False


def _place_random(
    objects: list[GameObject],
    *,
    name: str,
    sprite: list[str],
    count: int,
    region: tuple[int, int, int, int],
    solid: bool,
    player_start: Position,
    hitbox: tuple[int, int, int, int] | None = None,
    occludes: bool = False,
) -> None:
    width, height = _sprite_size(sprite)
    min_x, min_y, max_x, max_y = region
    max_x = max(min_x, max_x - width)
    max_y = max(min_y, max_y - height)
    attempts = count * 20

    for _ in range(attempts):
        if sum(1 for obj in objects if obj.name == name) >= count:
            break
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        if abs(x - player_start.x) < _SPAWN_CLEARANCE and abs(y - player_start.y) < _SPAWN_CLEARANCE:
            continue
        if _overlaps_any(objects, x, y, width, height):
            continue
        objects.append(
            GameObject.from_sprite(
                name=name,
                world_x=x,
                world_y=y,
                sprite=sprite,
                solid=solid,
                hitbox=hitbox,
                occludes=occludes,
            )
        )


def create_demo_world() -> World:
    """Initial playable world. Expand here as areas grow."""
    map_width, map_height = 200, 200
    player_start = Position(x=0, y=0)
    objects: list[GameObject] = []
    # Keep props near the starting area so they are visible while exploring.
    prop_region = (0, 0, 120, 60)

    _place_random(
        objects,
        name="tree",
        sprite=TREE,
        count=_TREE_COUNT,
        region=prop_region,
        solid=True,
        player_start=player_start,
        hitbox=TREE_HITBOX,
        occludes=True,
    )
    _place_random(
        objects,
        name="flower",
        sprite=FLOWER,
        count=_FLOWER_COUNT,
        region=prop_region,
        solid=False,
        player_start=player_start,
        occludes=False,
    )

    demo_map = Map(
        name="demo",
        width=map_width,
        height=map_height,
        objects=objects,
    )
    player = Player(position=player_start)
    player.inventory.add(WOOD, 12)
    player.inventory.add(STONE, 5)
    player.inventory.add(FISH, 1)

    return World(
        map=demo_map,
        player=player,
        camera=Camera(),
    )
