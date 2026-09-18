"""Google Wifi Status using mashumaro dataclasses."""

import ipaddress
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Literal, Union

from mashumaro import DataClassDictMixin
from mashumaro.config import BaseConfig


IPAddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]


@dataclass(frozen=True)
class GoogleWifiStatus(DataClassDictMixin):
    """Google Wifi status."""

    dns: "GoogleWifiStatus.DNS"
    software: "GoogleWifiStatus.Software"
    system: "GoogleWifiStatus.System"
    wan: "GoogleWifiStatus.WAN"

    class Config(BaseConfig):
        serialize_by_alias = True
        deserialize_by_alias = True

    @dataclass(frozen=True)
    class DNS(DataClassDictMixin):
        mode: Literal["automatic", "custom"]
        servers: list[IPAddress]

    @dataclass(frozen=True)
    class Software(DataClassDictMixin):
        software_version: str
        update_status: str
        update_required: bool
        update_progress: float

        class Config(BaseConfig):
            serialize_by_alias = True
            deserialize_by_alias = True
            aliases = {
                "software_version": "softwareVersion",
                "update_status": "updateStatus",
                "update_required": "updateRequired",
                "update_progress": "updateProgress",
            }

    @dataclass(frozen=True)
    class System(DataClassDictMixin):
        country_code: str
        model_id: str
        uptime: int
        last_restart: datetime = field(init=False)

        class Config(BaseConfig):
            serialize_by_alias = True
            deserialize_by_alias = True
            aliases = {
                "country_code": "countryCode",
                "model_id": "modelId",
            }

        def __post_init__(self):
            """Compute last_restart from uptime."""
            object.__setattr__(
                self,
                "last_restart",
                datetime.now() - timedelta(seconds=self.uptime),
            )

    @dataclass(frozen=True)
    class WAN(DataClassDictMixin):
        online: bool
        ethernet_link: bool
        gateway_ip_address: IPAddress
        local_ip_address: IPAddress
        ip_method: str
        ip_prefix_length: int
        name_servers: list[IPAddress]

        class Config(BaseConfig):
            serialize_by_alias = True
            deserialize_by_alias = True
            aliases = {
                "ethernet_link": "ethernetLink",
                "gateway_ip_address": "gatewayIpAddress",
                "local_ip_address": "localIpAddress",
                "ip_method": "ipMethod",
                "ip_prefix_length": "ipPrefixLength",
                "name_servers": "nameServers",
            }
