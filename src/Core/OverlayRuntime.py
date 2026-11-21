"""Pipeline orchestrator: wires ingest -> processors -> output drivers."""
from __future__ import annotations

from typing import Any

from loguru import logger

from src.Core.Ingest.MemoryIngest import MemoryIngest
from src.Core.Processors.ESPProcessor import ESPProcessor
from src.Core.Processors.AimAssistProcessor import AimAssistProcessor
from src.Core.Processors.RecoilProcessor import RecoilProcessor
from src.Output.OverlayDriver import OverlayDriver
from src.Output.InputDriver import InputDriver


class OverlayRuntime:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.ingest = MemoryIngest(config["process"])
        self.esp = ESPProcessor(config["esp"])
        self.aim = AimAssistProcessor(config["aim_assist"])
        self.recoil = RecoilProcessor(config["recoil"])
        self.overlay = OverlayDriver(config["overlay"])
        self.input = InputDriver(config["input"])
        self._running = True

    def boot(self) -> None:
        logger.info("booting combat-master-overlay runtime")
        self.ingest.attach()
        self.overlay.init_window()
        self.input.hook()
        logger.success("runtime ready")

    def run_forever(self) -> None:
        while self._running:
            snap = self.ingest.snapshot()
            entities = snap.entities
            if entities:
                esp_boxes = self.esp.process(entities, snap.view_matrix)
                self.overlay.draw_boxes(esp_boxes)
                target = self.aim.process(entities, snap.view_matrix, snap.crosshair)
                if target is not None:
                    self.input.move_to(target.screen_delta)
            self.recoil.process(self.input)

    def shutdown(self) -> None:
        self._running = False
        self.input.unhook()
        self.overlay.teardown()
        self.ingest.detach()
        logger.info("runtime stopped")