"""combat-master-overlay entry point."""
from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from src.Core.OverlayRuntime import OverlayRuntime
from src.Infrastructure.ConfigLoader import ConfigLoader


def main() -> int:
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add("logs/overlay_{time}.log", rotation="10 MB", retention=5)

    root = Path(__file__).resolve().parents[2]
    config = ConfigLoader(root / "config" / "default.yaml").load()

    runtime = OverlayRuntime(config)
    try:
        runtime.boot()
        runtime.run_forever()
    except KeyboardInterrupt:
        logger.warning("shutdown requested")
    finally:
        runtime.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())