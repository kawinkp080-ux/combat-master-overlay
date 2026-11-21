"""HWID spoofer helper for anti-cheat research (educational only)."""
from __future__ import annotations

import hashlib
import subprocess


class HwidSpoofer:
    def __init__(self, seed: str | None = None) -> None:
        self.seed = seed or "combat-master-overlay"

    def current_hwid(self) -> str:
        out = subprocess.check_output(
            ["wmic", "csproduct", "get", "UUID"], text=True)
        uuid = out.splitlines()[-1].strip()
        return hashlib.sha256((uuid + self.seed).encode()).hexdigest()

    def rotate(self) -> str:
        # Real rotation requires a signed driver — see docs/spoofer-setup.md
        return hashlib.sha256((self.seed + "rotated").encode()).hexdigest()