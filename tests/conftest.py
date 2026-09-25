"""Test fixtures for the API wrapper library."""

from collections.abc import AsyncGenerator, Generator
from typing import Any

import aiohttp
import pytest
from aioresponses import aioresponses

from googlewifiapi.api import GoogleWifiAPI
from googlewifiapi.const import DEFAULT_HOST, ENDPOINT

RESOURCE_URL = f"http://{DEFAULT_HOST}{ENDPOINT}"


@pytest.fixture
def mock_aioresponse() -> Generator[aioresponses, None, None]:
    """Activate aioresponses for the duration of a test."""
    with aioresponses() as m:
        yield m


@pytest.fixture
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Provide a real aiohttp session for aioresponses to intercept."""
    async with aiohttp.ClientSession() as s:
        yield s


@pytest.fixture
async def client(session: aiohttp.ClientSession) -> AsyncGenerator[GoogleWifiAPI, None]:
    """Provide a GoogleWifiAPI instance under test."""
    yield GoogleWifiAPI(host=DEFAULT_HOST, sess=session)


@pytest.fixture
async def mock_success(
    mock_aioresponse: aioresponses, normal_response: dict[str, Any]
) -> aioresponses:
    """Activate aioresponses for the duration of a test and mock a successful response."""
    mock_aioresponse.get(RESOURCE_URL, status=200, payload=normal_response)
    return mock_aioresponse


@pytest.fixture
async def mock_unreachable(mock_aioresponse: aioresponses) -> aioresponses:
    """Activate aioresponses for the duration of a test and mock an unreachable response."""
    mock_aioresponse.get(
        RESOURCE_URL, exception=aiohttp.ClientConnectionError("connection refused")
    )
    return mock_aioresponse


@pytest.fixture
def normal_response() -> dict[str, Any]:
    """Return a normal response from the API."""
    return {
        "dns": {"mode": "automatic", "servers": ["75.75.75.75", "75.75.76.76"]},
        "setupState": "GWIFI_OOBE_COMPLETE",
        "software": {
            "blockingUpdate": 1,
            "softwareVersion": "softwareVersion",
            "updateChannel": "stable-channel",
            "updateNewVersion": "0.0.0.0",
            "updateProgress": 0.0,
            "updateRequired": False,
            "updateStatus": "idle",
        },
        "system": {
            "countryCode": "us",
            "groupRole": "root",
            "hardwareId": "GALE [REDACTED]",
            "lan0Link": False,
            "ledAnimation": "CONNECTED",
            "ledIntensity": 6,
            "modelId": "modelId",
            "oobeDetailedStatus": "JOIN_AND_REGISTRATION_STAGE_DEVICE_ONLINE",
            "uptime": 3600,
        },
        "vorlonInfo": {"migrationMode": "voobed"},
        "wan": {
            "captivePortal": False,
            "ethernetLink": True,
            "gatewayIpAddress": "10.0.0.1",
            "invalidCredentials": False,
            "ipAddress": True,
            "ipMethod": "dhcp",
            "ipPrefixLength": 24,
            "leaseDurationSeconds": 1,
            "localIpAddress": "10.0.0.10",
            "nameServers": ["75.75.75.75", "75.75.76.76"],
            "online": True,
            "pppoeDetected": False,
            "vlanScanAttemptCount": 0,
            "vlanScanComplete": True,
        },
    }
