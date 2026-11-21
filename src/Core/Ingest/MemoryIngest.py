"""Reads Combat Master entity list + view matrix via ReadProcessMemory."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pymem
from loguru import logger

from src.Core.Models.Entity import Entity
from src.Core.Models.Snapshot import Snapshot
from src.Infrastructure.offsets.OffsetTable import OffsetTable


@dataclass
class MemoryIngest:
    process_cfg: dict[str, Any]
    offsets: OffsetTable = field(init=False)
    pm: pymem.Pymem | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.offsets = OffsetTable.load(self.process_cfg.get("build_id", "latest"))

    def attach(self) -> None:
        name = self.process_cfg["exe_name"]
        try:
            self.pm = pymem.Pymem(name)
            logger.info("attached to {}", name)
        except pymem.exception.ProcessNotFound:
            raise RuntimeError(f"Combat Master process {name!r} not running")

    def detach(self) -> None:
        self.pm = None

    def snapshot(self) -> Snapshot:
        if self.pm is None:
            return Snapshot(entities=[], view_matrix=[0.0] * 16, crosshair=(0, 0))
        base = self.pm.base_address + self.offsets.entity_list
        view = self.pm.read_float(base + self.offsets.view_matrix, 16)
        entities: list[Entity] = []
        for i in range(self.offsets.max_entities):
            addr = base + i * self.offsets.entity_stride
            try:
                hp = self.pm.read_int(addr + self.offsets.health)
            except Exception:
                continue
            if hp <= 0:
                continue
            pos = self.pm.read_float(addr + self.offsets.position, 3)
            entities.append(Entity(index=i, health=hp, position=tuple(pos)))
        return Snapshot(entities=entities, view_matrix=list(view), crosshair=(960, 540))