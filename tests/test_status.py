"""Test that the API wrapper can fetch and interpret the router status."""

from ipaddress import IPv4Address
from typing import Any
from unittest.mock import patch

import aiohttp
import pytest
from aioresponses import aioresponses

from googlewifiapi.api import GoogleWifiAPI
from googlewifiapi.exception import (
    GoogleWifiClientError,
    GoogleWifiDataValidationError,
    GoogleWifiException,
)
from googlewifiapi.status import GoogleWifiStatus

from .conftest import RESOURCE_URL


def test_schema_validation(normal_response: dict[str, Any]) -> None:
    """Test that the GoogleWifiStatus schema validates sample data from a normal response correctly."""
    status = GoogleWifiStatus.from_dict(normal_response)

    assert status.dns.mode == "automatic"
    assert status.dns.servers == [
        IPv4Address("75.75.75.75"),
        IPv4Address("75.75.76.76"),
    ]

    assert status.software.software_version == "softwareVersion"
    assert status.software.update_status == "idle"
    assert status.software.update_required is False
    assert status.software.update_progress == 0.0

    assert status.system.country_code == "us"
    assert isinstance(status.system.country_code, str)
    assert status.system.model_id == "modelId"
    assert status.system.uptime == 3600
    assert status.system.last_restart is not None

    assert status.wan.online is True
    assert status.wan.ethernet_link is True
    assert status.wan.gateway_ip_address == IPv4Address("10.0.0.1")
    assert status.wan.local_ip_address == IPv4Address("10.0.0.10")
    assert status.wan.ip_method == "dhcp"
    assert status.wan.ip_prefix_length == 24
    assert status.wan.name_servers == [
        IPv4Address("75.75.75.75"),
        IPv4Address("75.75.76.76"),
    ]


class TestApiUpdate:
    """Tests whether the API wrapper can update with different conditions."""

    @pytest.mark.asyncio
    async def test_async_update_success(
        self,
        mock_success: aioresponses,
        client: GoogleWifiAPI,
        normal_response: dict[str, Any],
    ) -> None:
        """Test that a normal response updates the client's data correctly."""
        await client.async_update()

        assert client.raw_data == normal_response
        assert isinstance(client.data, GoogleWifiStatus)

    @pytest.mark.asyncio
    async def test_async_update_invalid_data_raises_validation_error(
        self,
        mock_aioresponse: aioresponses,
        client: GoogleWifiAPI,
        normal_response: dict[str, Any],
    ) -> None:
        """Test that a response missing required fields raises a validation error."""
        broken_response = {k: v for k, v in normal_response.items() if k != "wan"}
        mock_aioresponse.get(RESOURCE_URL, status=200, payload=broken_response)

        with pytest.raises(GoogleWifiDataValidationError):
            await client.async_update()

    @pytest.mark.asyncio
    async def test_async_update_empty_response_raises_validation_error(
        self, mock_aioresponse: aioresponses, client: GoogleWifiAPI
    ) -> None:
        """Test that an empty/null response body raises a validation error."""
        mock_aioresponse.get(RESOURCE_URL, status=200, payload=None)

        with pytest.raises(GoogleWifiDataValidationError):
            await client.async_update()

    @pytest.mark.asyncio
    async def test_async_update_invalid_json_raises_client_error(
        self, mock_aioresponse: aioresponses, client: "GoogleWifiAPI"
    ) -> None:
        """Test that a non-JSON response body raises a client error."""
        mock_aioresponse.get(
            RESOURCE_URL,
            status=200,
            body="not valid json{{{",
            content_type="application/json",
        )

        with pytest.raises(GoogleWifiClientError):
            await client.async_update()

    @pytest.mark.asyncio
    async def test_async_update_connection_error_raises_client_error(
        self, mock_unreachable: aioresponses, client: "GoogleWifiAPI"
    ) -> None:
        """Test that a connection failure raises a client error."""
        with pytest.raises(GoogleWifiClientError):
            await client.async_update()

    @pytest.mark.asyncio
    async def test_async_update_timeout_raises_client_error(
        self, mock_aioresponse: aioresponses, client: "GoogleWifiAPI"
    ) -> None:
        """Test that a request timeout raises a client error."""
        mock_aioresponse.get(
            RESOURCE_URL,
            exception=aiohttp.ServerTimeoutError("request timed out"),
        )

        with pytest.raises(GoogleWifiClientError):
            await client.async_update()

    @pytest.mark.asyncio
    async def test_async_update_unexpected_error_raises_generic_exception(
        self,
        mock_success: aioresponses,
        client: GoogleWifiAPI,
    ) -> None:
        """Test that an unexpected failure in schema parsing raises the generic exception."""
        with (
            patch(
                "googlewifiapi.status.GoogleWifiStatus.from_dict",
                side_effect=RuntimeError("boom"),
            ),
            pytest.raises(GoogleWifiException),
        ):
            await client.async_update()
