"""Mouse / keyboard injection driver (SendInput based)."""
from __future__ import annotations

import ctypes
from dataclasses import dataclass, field

import keyboard


@dataclass(slots=True)
class Target:
    screen_delta: tuple[float, float]
    entity_index: int


@dataclass
class InputDriver:
    cfg: dict
    _hooked: bool = field(default=False, init=False)

    def hook(self) -> None:
        keyboard.on_press_key(self.cfg.get("toggle_key", "f4"),
                              lambda _: self._toggle(), suppress=False)
        self._hooked = True

    def unhook(self) -> None:
        keyboard.unhook_all()
        self._hooked = False

    def _toggle(self) -> None:
        self.cfg["enabled"] = not self.cfg.get("enabled", True)

    def move_to(self, delta: tuple[float, float]) -> None:
        if not self.cfg.get("enabled", True):
            return
        dx, dy = int(delta[0]), int(delta[1])
        ctypes.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)

    def inject_move(self, dx: float, dy: float) -> None:
        ctypes.windll.user32.mouse_event(0x0001, int(dx), int(dy), 0, 0)

    def left_mouse_down(self) -> bool:
        return bool(ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000)

    def recoil_accumulator(self, pattern: str) -> tuple[float, float]:
        table = {"ak": (0.0, 2.4), "m4": (0.0, 1.8), "smg": (0.0, 1.2)}
        return table.get(pattern, (0.0, 1.5))

    def reset_recoil(self) -> None:
        return None