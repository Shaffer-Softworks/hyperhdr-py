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

### New in v0.1.0 (HyperHDR v20–v22)

- **Average color** — Average color of current LED output
- **Smoothing control** — Adjust smoothing, including v22 interpolators
- **HDR tone mapping** — Tone mapping mode and automatic detection (v21+)
- **Service discovery** — Discover HyperHDR instances on the network
- **Current LED colors** — Read colors being sent to LEDs
- **Performance benchmarking** — Run server benchmarks
- **Config management** — Save/load the configuration database

## Installation

```bash
pip install hyperhdr-py-sickkick
```

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

## LED streaming (WebSocket)

Install dependencies before using the stream helpers:

```bash
pip install aiohttp
```

If you use `convert_to_jpeg=True`, install Pillow as well, or use the extras:

```bash
pip install "hyperhdr-py-sickkick[stream]"
pip install "hyperhdr-py-sickkick[stream-jpeg]"
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
