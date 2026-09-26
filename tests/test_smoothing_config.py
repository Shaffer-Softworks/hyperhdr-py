"""Tests for v22 config get/set and smoothing helpers."""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest

from hyperhdr import const
from hyperhdr.client import HyperHDRClient


@pytest.mark.asyncio
async def test_send_set_smoothing_time_only_rpc() -> None:
    """Legacy smoothing RPC must only send subcommand + time."""
    client = HyperHDRClient("127.0.0.1")
    sent: list[dict[str, Any]] = []

    async def capture(data: dict[str, Any]) -> bool:
        sent.append(data)
        return True

    client._async_send_json = AsyncMock(side_effect=capture)  # type: ignore[method-assign]

    assert await client.async_send_set_smoothing(time=150) is True
    assert sent[0][const.KEY_COMMAND] == const.KEY_SMOOTHING
    assert sent[0][const.KEY_SUBCOMMAND] == const.KEY_SMOOTHING_SUBCOMMAND_ALL
    assert sent[0][const.KEY_SMOOTHING_TIME] == 150
    assert "smoothingType" not in sent[0]
    assert "decay" not in sent[0]


@pytest.mark.asyncio
async def test_send_set_config_requires_config() -> None:
    """setconfig must include a config fragment."""
    client = HyperHDRClient("127.0.0.1")
    with pytest.raises(ValueError, match="config"):
        await client.async_send_set_config()


@pytest.mark.asyncio
async def test_send_set_config_payload() -> None:
    """setconfig wraps fragment under config/setconfig."""
    client = HyperHDRClient("127.0.0.1")
    sent: list[dict[str, Any]] = []

    async def capture(data: dict[str, Any]) -> bool:
        sent.append(data)
        return True

    client._async_send_json = AsyncMock(side_effect=capture)  # type: ignore[method-assign]

    fragment = {"smoothing": {"type": "HybridRgbInterpolator", "time_ms": 150}}
    assert await client.async_send_set_config(config=fragment) is True
    assert sent[0][const.KEY_COMMAND] == const.KEY_CONFIG
    assert sent[0][const.KEY_SUBCOMMAND] == const.KEY_SET_CONFIG
    assert sent[0][const.KEY_CONFIG] == fragment


@pytest.mark.asyncio
async def test_get_smoothing_config_caches() -> None:
    """get_smoothing_config reads info.smoothing and caches it."""
    client = HyperHDRClient("127.0.0.1")
    smooth = {
        "antiFlickeringFilter": True,
        "continuousOutput": True,
        "type": "HybridRgbInterpolator",
        "time_ms": 150,
        "updateFrequency": 50,
        "damping": 26,
        "stiffness": 150,
        "smoothingFactor": 0,
        "enable": True,
    }

    async def fake_get_config() -> dict[str, Any]:
        return {
            const.KEY_SUCCESS: True,
            const.KEY_COMMAND: f"{const.KEY_CONFIG}-{const.KEY_GET_CONFIG}",
            const.KEY_INFO: {const.KEY_SMOOTHING: smooth},
        }

    client.async_get_config = AsyncMock(side_effect=fake_get_config)  # type: ignore[method-assign]

    result = await client.async_get_smoothing_config()
    assert result == smooth
    assert client.smoothing == smooth


@pytest.mark.asyncio
async def test_update_smoothing_config_merge_patch() -> None:
    """update_smoothing_config merges fields into a full smoothing object."""
    client = HyperHDRClient("127.0.0.1")
    current = {
        "antiFlickeringFilter": True,
        "continuousOutput": True,
        "type": "HybridRgbInterpolator",
        "time_ms": 150,
        "updateFrequency": 50,
        "damping": 26,
        "stiffness": 150,
        "smoothingFactor": 0,
        "enable": True,
        "y_limit": 0.03,
    }
    client._update_smoothing(current)

    set_calls: list[dict[str, Any]] = []

    async def fake_set_config(**kwargs: Any) -> dict[str, Any]:
        set_calls.append(kwargs)
        return {
            const.KEY_SUCCESS: True,
            const.KEY_COMMAND: f"{const.KEY_CONFIG}-{const.KEY_SET_CONFIG}",
        }

    async def fake_get_smoothing() -> dict[str, Any]:
        patched = dict(current)
        patched["antiFlickeringFilter"] = False
        client._update_smoothing(patched)
        return patched

    client.async_set_config = AsyncMock(side_effect=fake_set_config)  # type: ignore[method-assign]
    client.async_get_smoothing_config = AsyncMock(  # type: ignore[method-assign]
        side_effect=fake_get_smoothing
    )

    result = await client.async_update_smoothing_config(antiFlickeringFilter=False)
    assert result is not None
    assert result["antiFlickeringFilter"] is False
    assert set_calls[0]["config"]["smoothing"]["antiFlickeringFilter"] is False
    assert set_calls[0]["config"]["smoothing"]["type"] == "HybridRgbInterpolator"
    assert set_calls[0]["config"]["smoothing"]["time_ms"] == 150
