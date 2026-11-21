# Contributing to combat-master-overlay

Thanks for your interest in improving the Combat Master overlay project.

## Ground rules

- **Educational / research use only.** Combat Master Cheats overlays are meant for offline
  reverse-engineering research and cheat-detection development. Do not ship builds that
  target live ranked servers.
- No obfuscated blobs, packed DLLs, or prebuilt binaries in PRs. Source-only.
- Keep offset tables and signature scans in `src/Infrastructure/offsets/` — never inline in
  processors.

## Workflow

1. Fork and branch off `main` (`feat/esp-chams`, `fix/aimbot-smoothing`).
2. Run `python -m pytest tests/` before opening a PR.
3. Run `python scripts/refresh_offsets.py --dry-run` if you touched the schema reader.
4. Describe which Combat Master build (Steam build ID) you tested against.

## Code style

- Python 3.11+, type hints on public functions.
- `ruff` for linting, `black -l 100` for formatting.
- Worker pipelines should be small, single-purpose classes under `src/Core/Processors/`.

## Reporting offset breakage

Attach `dumps/client_info.json` output from `scripts/dump_client_info.py` — **not** full memory
dumps (they contain your account tokens).