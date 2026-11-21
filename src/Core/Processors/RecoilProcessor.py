"""Counteracts vertical spray by injecting a downward correction per shot."""
from __future__ import annotations

from dataclasses import dataclass

from src.Output.InputDriver import InputDriver


@dataclass
class RecoilProcessor:
    cfg: dict

    def process(self, driver: InputDriver) -> None:
        if not self.cfg.get("enabled", True):
            return
        if not driver.left_mouse_down():
            driver.reset_recoil()
            return
        pattern = self.cfg.get("pattern", "ak")
        strength = self.cfg.get("strength", 0.35)
        dx, dy = driver.recoil_accumulator(pattern)
        driver.inject_move(dx * strength, dy * strength)