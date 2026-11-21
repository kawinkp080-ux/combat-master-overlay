"""Scans CombatMaster.exe for the entity-list signature and rewrites latest.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pymem

SIGNATURE = b"\x48\x8B\x05????\x48\x85\xC0\x74"


def scan(exe_name: str) -> int:
    pm = pymem.Pymem(exe_name)
    module = pymem.process.module_from_name(pm.process_handle, exe_name)
    data = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    for i in range(len(data) - len(SIGNATURE)):
        if data[i:i + 4] == SIGNATURE[:4]:
            return module.lpBaseOfDll + i
    raise RuntimeError("signature not found — Combat Master may have updated")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--exe", default="CombatMaster.exe")
    ap.add_argument("--build-id", default="latest")
    args = ap.parse_args()
    addr = scan(args.exe)
    if args.dry_run:
        print(f"signature at 0x{addr:x}")
        return
    cache = Path(__file__).parents[1] / "src/Infrastructure/offsets/cache"
    tbl = json.loads((cache / "latest.json").read_text())
    tbl["entity_list"] = addr
    (cache / f"{args.build_id}.json").write_text(json.dumps(tbl, indent=2))


if __name__ == "__main__":
    main()