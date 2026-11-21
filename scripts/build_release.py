"""Wraps PyInstaller for the Combat Master overlay release build."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean",
        "--name", "combat-master-overlay",
        "--windowed",
        "--add-data", f"{ROOT / 'config'};config",
        "--add-data", f"{ROOT / 'src/Infrastructure/offsets/cache'};offsets",
        str(ROOT / "src/App/main.py"),
    ]
    subprocess.check_call(cmd)


if __name__ == "__main__":
    run()