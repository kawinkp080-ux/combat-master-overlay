"""Transparent always-on-top pygame window that renders ESP boxes."""
from __future__ import annotations

import ctypes
from dataclasses import dataclass

import pygame
from loguru import logger


@dataclass
class Box:
    x: float
    y: float
    w: float
    h: float
    color: tuple[int, int, int]
    label: str = ""


class OverlayDriver:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.screen: pygame.Surface | None = None
        self.font: pygame.font.Font | None = None

    def init_window(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x80000 | 0x20 | 0x8)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, 0x2)
        self.font = pygame.font.SysFont("Consolas", 12)
        logger.info("overlay window ready")

    def draw_boxes(self, boxes: list[Box]) -> None:
        if self.screen is None:
            return
        self.screen.fill((0, 0, 0))
        for b in boxes:
            pygame.draw.rect(self.screen, b.color, (b.x, b.y, b.w, b.h), 1)
            if self.font and b.label:
                self.screen.blit(self.font.render(b.label, True, b.color), (b.x, b.y - 12))
        pygame.display.flip()

    def teardown(self) -> None:
        pygame.quit()