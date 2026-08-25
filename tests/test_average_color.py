"""Tests for average-color JSON-RPC payload."""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest

from hyperhdr import const
from hyperhdr.client import HyperHDRClient


@pytest.mark.asyncio
async def test_send_get_average_color_uses_current_state() -> None:
    """Average color must use current-state/average-color, not calculate-colors."""
    client = HyperHDRClient("127.0.0.1", instance=2)
    sent: list[dict[str, Any]] = []

    async def capture(data: dict[str, Any]) -> bool:
        sent.append(data)
        return True

    client._async_send_json = AsyncMock(side_effect=capture)  # type: ignore[method-assign]

    assert await client.async_send_get_average_color() is True
    assert len(sent) == 1
    assert sent[0][const.KEY_COMMAND] == const.KEY_CURRENT_STATE
    assert sent[0][const.KEY_SUBCOMMAND] == const.KEY_AVERAGE_COLOR_SUBCOMMAND
    assert sent[0][const.KEY_INSTANCE] == 2
    assert sent[0][const.KEY_COMMAND] != const.KEY_AVERAGE_COLOR
    assert sent[0].get(const.KEY_SUBCOMMAND) != const.KEY_CURRENT_COLORS


@pytest.mark.asyncio
async def test_send_get_average_color_instance_override() -> None:
    """Callers can override instance via kwargs."""
    client = HyperHDRClient("127.0.0.1", instance=0)
    sent: list[dict[str, Any]] = []

    async def capture(data: dict[str, Any]) -> bool:
        sent.append(data)
        return True

    client._async_send_json = AsyncMock(side_effect=capture)  # type: ignore[method-assign]

    assert await client.async_send_get_average_color(instance=5) is True
    assert sent[0][const.KEY_INSTANCE] == 5
