"""Finds the closest on-screen target and returns the delta needed to snap."""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from src.Core.Models.Entity import Entity
from src.Output.InputDriver import Target


@dataclass
class AimAssistProcessor:
    cfg: dict

    def process(self, entities: list[Entity], view_matrix: list[float],
                crosshair: tuple[int, int]) -> Target | None:
        vm = np.array(view_matrix, dtype=np.float32).reshape(4, 4)
        best: Target | None = None
        best_dist = self.cfg.get("fov_px", 180)
        for ent in entities:
            if ent.health <= 0:
                continue
            clip = vm @ np.array([*ent.position, 1.0], dtype=np.float32)
            if clip[3] <= 0.0:
                continue
            ndc = clip[:3] / clip[3]
            sx = (ndc[0] + 1.0) * 0.5 * 1920
            sy = (1.0 - ndc[1]) * 0.5 * 1080
            dx, dy = sx - crosshair[0], sy - crosshair[1]
            dist = math.hypot(dx, dy)
            if dist < best_dist:
                best_dist = dist
                smooth = self.cfg.get("smoothing", 1.0)
                best = Target(screen_delta=(dx / smooth, dy / smooth), entity_index=ent.index)
        return best