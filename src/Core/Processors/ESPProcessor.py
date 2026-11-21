"""Projects 3D entity positions to screen-space boxes for the overlay."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from src.Core.Models.Entity import Entity
from src.Output.OverlayDriver import Box


@dataclass
class ESPProcessor:
    cfg: dict

    def process(self, entities: Iterable[Entity], view_matrix: list[float]) -> list[Box]:
        vm = np.array(view_matrix, dtype=np.float32).reshape(4, 4)
        boxes: list[Box] = []
        for ent in entities:
            if self.cfg.get("team_filter") and ent.team == self.cfg.get("my_team"):
                continue
            clip = vm @ np.array([*ent.position, 1.0], dtype=np.float32)
            if clip[3] <= 0.01:
                continue
            ndc = clip[:3] / clip[3]
            sx = (ndc[0] + 1.0) * 0.5 * 1920
            sy = (1.0 - ndc[1]) * 0.5 * 1080
            h = max(8.0, 240.0 / max(1.0, clip[3]))
            w = h * 0.5
            boxes.append(Box(x=sx - w / 2, y=sy - h, w=w, h=h,
                             color=self._color_for(ent), label=f"hp{ent.health}"))
        return boxes

    def _color_for(self, ent: Entity) -> tuple[int, int, int]:
        if ent.health < 25:
            return (255, 40, 40)
        return (40, 220, 90)