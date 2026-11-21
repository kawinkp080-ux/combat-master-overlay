"""Loads per-build offset tables from JSON so patches don't require rebuilds."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

CACHE = Path(__file__).parent / "cache"


@dataclass(frozen=True)
class OffsetTable:
    entity_list: int
    view_matrix: int
    entity_stride: int
    max_entities: int
    health: int
    position: int

    @classmethod
    def load(cls, build_id: str) -> "OffsetTable":
        path = CACHE / f"{build_id}.json"
        if not path.exists():
            path = CACHE / "latest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)