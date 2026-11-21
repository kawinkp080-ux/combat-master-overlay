from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Entity:
    index: int
    health: int
    position: tuple[float, float, float]
    team: int = 0
    name: str = ""

    @property
    def is_alive(self) -> bool:
        return self.health > 0