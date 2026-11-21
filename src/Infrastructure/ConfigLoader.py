from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ProcessCfg(BaseModel):
    exe_name: str = "CombatMaster.exe"
    build_id: str = "latest"


class RuntimeConfig(BaseModel):
    process: ProcessCfg = Field(default_factory=ProcessCfg)
    esp: dict[str, Any] = Field(default_factory=dict)
    aim_assist: dict[str, Any] = Field(default_factory=dict)
    recoil: dict[str, Any] = Field(default_factory=dict)
    overlay: dict[str, Any] = Field(default_factory=dict)
    input: dict[str, Any] = Field(default_factory=dict)


class ConfigLoader:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        raw = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
        return RuntimeConfig(**raw).model_dump()