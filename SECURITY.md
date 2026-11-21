# Security Policy

## Scope

`combat-master-overlay` is a research-grade external overlay for Combat Master.
We take reports about the **project itself** seriously — e.g. arbitrary code execution
in the injector, unsafe pickle deserialization in the config loader, or path traversal
in the offset-cache packer.

Out of scope:
- Combat Master's own anti-cheat detections of this tool.
- Bans resulting from use of builds compiled from this repo.

## Reporting

Email `security@combat-master-overlay.dev` (PGP key in `docs/pgp.txt`) with:
- Affected component (e.g. `Infrastructure/Injector`)
- Reproduction steps on a clean Windows 11 VM
- Repo commit hash

We aim to acknowledge within 72 hours. Do **not** open public GitHub issues for
vulnerabilities in the injector or driver loader.

## Build hygiene

- Never commit `config/local.yaml`.
- Never commit signed drivers — users must supply their own legitimate HWID spoofer certs.
- Verify release hashes against `docs/release-checksums.txt` before running any build.