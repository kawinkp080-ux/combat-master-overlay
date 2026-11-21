from __future__ import annotations

from dataclasses import dataclass

from src.Core.Models.Entity import Entity


@dataclass(slots=True)
class Snapshot:
    entities: list[Entity]
    view_matrix: list[float]
    crosshair: tuple[int, int]

    @property
    def visible_entities(self) -> list[Entity]:
        return [e for e in self.entities if e.is_alive]