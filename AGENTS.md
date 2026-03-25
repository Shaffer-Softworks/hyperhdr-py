# Agent context: hyperhdr-py

## What this is

Python client for **[HyperHDR](https://github.com/awawa-dev/HyperHDR)** ambient lighting. It extends **[hyperion-py](https://github.com/dermotduffy/hyperion-py)** (Dermot Duffy) with HyperHDR-specific behavior and versions **v19–v22+**.

## Install vs import

| | Value |
|---|--------|
| **PyPI package** | `hyperhdr-py-sickkick` |
| **Install** | `pip install hyperhdr-py-sickkick` |
| **Import** | `from hyperhdr import client, const` (and `hyperhdr.stream` for WebSocket helpers) |
| **Optional extras** | `[stream]` → `aiohttp`; `[stream-jpeg]` → `aiohttp` + `Pillow` |

## Repository

- **Canonical remote**: `https://github.com/sickkick/hyperhdr-py`
- Keep user-facing links (`README`, badges, raw images) consistent with this repo, not older forks.

## Layout

- `hyperhdr/` — library code; `client.py` has JSON API methods (`async_*`).
- `hyperhdr/stream.py` — LED color / gradient WebSocket streaming.
- `examples/stream_leds.py` — streaming example.
- `RELEASING.md` — PyPI release via tags + GitHub Actions.

## Documentation

- **README.md** — quick start, install, streaming snippet, pointers to official API docs.
- **HyperHDR JSON API** — https://docs.hyperhdr-project.org/en/json/ (source of truth for request/response shapes).
- Threaded wrapper: `ThreadedHyperHDRClient` (sync-style API, no `async_` prefix).

## Tooling

- **Deps / build**: Poetry (`pyproject.toml`).
- **Tests**: `pytest` (see `[tool.pytest.ini_options]`; coverage threshold in `[tool.coverage.report]`).

## Recent doc maintenance (2025-03)

README was shortened: removed a large HTML-commented copy of legacy docs (wrong PyPI name and third-party repo links). Prefer the official JSON docs + `hyperhdr/client.py` for API detail.
