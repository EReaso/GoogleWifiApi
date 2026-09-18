"""Exceptions for the Google Wifi API Wrapper."""


class GoogleWifiException(Exception):
    """Raised when there is a generic exception while wrapping the API."""


class GoogleWifiDataValidationError(GoogleWifiException):
    """Raised when the data cannot be validated."""


class GoogleWifiClientError(GoogleWifiException):
    """Raised when the connection fails in some way."""
