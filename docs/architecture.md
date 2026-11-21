# Architecture

combat-master-overlay is a pipeline/worker overlay:

```
MemoryIngest --> ESPProcessor  --> OverlayDriver (pygame overlay)
             --> AimAssistProcessor --> InputDriver (mouse injection)
             --> RecoilProcessor    --> InputDriver
```

- **Ingest** (`src/Core/Ingest`) reads entity list + view matrix via `pymem`.
- **Processors** (`src/Core/Processors`) are pure functions of `Snapshot` -> output DTO.
- **Drivers** (`src/Output`) own OS handles. Two drivers: overlay renderer, input injector.
- **Infrastructure** holds offsets, config, injector, HWID spoofer.

Offsets live in `src/Infrastructure/offsets/cache/<build_id>.json` and are regenerated
by `scripts/refresh_offsets.py` after each Combat Master patch.