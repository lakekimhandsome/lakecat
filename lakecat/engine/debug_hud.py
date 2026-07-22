from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from lakecat import __version__

if TYPE_CHECKING:
    from lakecat.world.world import World


@dataclass
class DebugStats:
    """Frame / runtime metrics that are not part of World state.

    Add new fields here as the HUD grows (render_ms, memory_mb, colliding, ...).
    """

    fps: float = 0.0


class DebugHud:
    """Builds screen-space debug lines. Drawing stays in Renderer."""

    def lines(self, world: World, stats: DebugStats) -> list[str]:
        player = world.player.position
        camera = world.camera
        return [
            f"Lakecat ({__version__})",
            f"Map : {world.map.name}",
            f"Player : ({player.x}, {player.y})",
            f"Camera : ({camera.x}, {camera.y})",
            f"FPS : {stats.fps:.0f}",
            f"Objects : {len(world.map.objects)}",
        ]
