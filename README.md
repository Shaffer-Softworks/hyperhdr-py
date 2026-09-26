# hyperhdr-py

A Python library for controlling [HyperHDR](https://github.com/awawa-dev/HyperHDR) ambient lighting systems.

This library builds on [Dermot Duffy](https://github.com/dermotduffy)’s [hyperion-py](https://github.com/dermotduffy/hyperion-py).

<img src="https://github.com/sickkick/hyperhdr-py/blob/main/images/hyperhdrlogo.png?raw=true"
     alt="HyperHDR logo"
     width="160"
     align="left" />

## Features

- Full async support with `asyncio`
- Connect to the HyperHDR JSON API
- Control colors, effects, components, and more
- Subscribe to real-time state updates
- Support for HyperHDR v19 through v22+
- Optional WebSocket LED color/gradient streaming (requires `aiohttp`)

### Notable APIs (v0.1–v0.2)

- **Average color** — `async_get_average_color()` via `current-state` / `average-color` (v20+)
- **Smoothing** — legacy time RPC (`async_set_smoothing`) plus v22 config helpers (`async_get_smoothing_config` / `async_update_smoothing_config`)
- **Config set** — authenticated `async_set_config` for config fragments (v22+)
- **HDR tone mapping** — mode and automatic detection (v21+)
- **Service discovery** — discover HyperHDR instances on the network
- **LED WebSocket streams** — `HyperHDRLedColorsStream` / `HyperHDRLedGradientStream` with token or admin-password auth
- **Performance benchmarking** — run server benchmarks
- **Config database** — save/load the configuration database

## Installation

```bash
pip install hyperhdr-py-sickkick
```

Current release: **0.2.3**.

## Quick start

```python
import asyncio
from hyperhdr import client, const

async def main():
    async with client.HyperHDRClient("hyperhdr.local") as hc:
        if hc:
            adjustment = hc.adjustment
            if adjustment:
                print(f"Brightness: {adjustment[0][const.KEY_BRIGHTNESS]}%")

            await hc.async_set_color(color=[255, 0, 0], priority=50)
            await hc.async_set_effect(effect={"name": "Rainbow swirl"}, priority=50)

asyncio.run(main())
```

### Smoothing (HyperHDR v22)

Use the legacy RPC only to change smoothing time. For type, anti-flicker, continuous output, and hybrid knobs, use the config helpers (admin auth required):

```python
# Time only (validated JSON-RPC)
await hc.async_set_smoothing(time=150)

# Full smoothing object via config/getconfig + config/setconfig
await hc.async_update_smoothing_config(
    type=const.SMOOTHING_TYPE_HYBRID_RGB_INTERPOLATOR,
    time_ms=150,
    antiFlickeringFilter=True,
    continuousOutput=True,
)
```

## LED streaming (WebSocket)

Install dependencies before using the stream helpers:

```bash
pip install "hyperhdr-py-sickkick[stream]"
pip install "hyperhdr-py-sickkick[stream-jpeg]"  # if convert_to_jpeg=True
```

```python
import asyncio
from hyperhdr.stream import HyperHDRLedColorsStream, HyperHDRLedGradientStream

async def main():
    led_colors = HyperHDRLedColorsStream("hyperhdr.local", token="YOUR_TOKEN")
    await led_colors.start()
    frame = await led_colors.wait_for_frame()
    if frame and frame.raw:
        print("LED bytes:", len(frame.raw))
    await led_colors.stop()

    led_gradient = HyperHDRLedGradientStream("hyperhdr.local")
    async for frame in led_gradient.frames():
        print("Gradient update:", frame.source)
        break
    await led_gradient.stop()

asyncio.run(main())
```

See [`examples/stream_leds.py`](examples/stream_leds.py) for a runnable script.

## API and data model

Request and response shapes follow the [HyperHDR JSON API](https://docs.hyperhdr-project.org/en/json/). Async methods on `HyperHDRClient` are named `async_*` and match that API; see [`hyperhdr/client.py`](https://github.com/sickkick/hyperhdr-py/blob/main/hyperhdr/client.py) for the full list.

For threaded use without `asyncio`, use `ThreadedHyperHDRClient` (same method names without the `async_` prefix). After `start()`, call `wait_for_client_init()` before connecting.

## Credits

Thanks to Dermot Duffy for [hyperion-py](https://github.com/dermotduffy/hyperion-py), which this project extends.

Feel free to open an issue if you run into problems.
