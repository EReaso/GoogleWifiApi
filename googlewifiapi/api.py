"""Google Wifi API wrapper."""

from typing import Any

import aiohttp
from yarl import URL

from .const import DEFAULT_HOST, ENDPOINT
from .exception import (
    GoogleWifiClientError,
    GoogleWifiDataValidationError,
    GoogleWifiException,
)
from .status import GoogleWifiStatus


class GoogleWifiAPI:
    """Get the latest data and update the states."""

    raw_data: dict[str, Any] | None = None
    available: bool = True
    _resource: URL
    data: GoogleWifiStatus | None = None
    sess: aiohttp.ClientSession

    def __init__(
        self, host: str = DEFAULT_HOST, sess: aiohttp.ClientSession | None = None
    ) -> None:
        """Initialize the API wrapper."""
        self._resource = URL(f"http://{host}{ENDPOINT}")
        self.sess = sess or aiohttp.ClientSession()

    async def async_update(self) -> GoogleWifiStatus:
        """Get the latest data from the router."""
        try:
            resp = await self.sess.get(self._resource)
            raw_data = await resp.json()
        except (aiohttp.ClientError, ValueError) as err:
            raise GoogleWifiClientError() from err

        if not isinstance(raw_data, dict):
            raise GoogleWifiDataValidationError(
                f"The router provided data that could not be validated. "
                f"Raw data: {raw_data}"
            )

        self.raw_data = raw_data
        try:
            self.data = GoogleWifiStatus.from_dict(raw_data)
            return self.data
        except (LookupError, TypeError, ValueError) as err:
            raise GoogleWifiDataValidationError(
                f"The router provided data that could not be validated. "
                f"Raw data: {raw_data}"
            ) from err
        except Exception as err:
            raise GoogleWifiException() from err
