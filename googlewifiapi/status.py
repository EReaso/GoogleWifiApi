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
    setup_state: str
    software: "GoogleWifiStatus.Software"
    system: "GoogleWifiStatus.System"
    vorlon_info: "GoogleWifiStatus.VorlonInfo"
    wan: "GoogleWifiStatus.WAN"

    class Config(BaseConfig):
        """Configure status serialization."""

        serialize_by_alias = True
        deserialize_by_alias = True
        aliases = {
            "setup_state": "setupState",
            "vorlon_info": "vorlonInfo",
        }

    @dataclass(frozen=True)
    class DNS(DataClassDictMixin):
        """DNS status."""

        mode: Literal["automatic", "custom"]
        servers: list[IPAddress]

    @dataclass(frozen=True)
    class Software(DataClassDictMixin):
        """Software status."""

        blocking_update: int
        software_version: str
        update_channel: str
        update_new_version: str
        update_progress: float
        update_required: bool
        update_status: str

        class Config(BaseConfig):
            """Configure software serialization."""

            serialize_by_alias = True
            deserialize_by_alias = True
            aliases = {
                "blocking_update": "blockingUpdate",
                "software_version": "softwareVersion",
                "update_channel": "updateChannel",
                "update_new_version": "updateNewVersion",
                "update_progress": "updateProgress",
                "update_required": "updateRequired",
                "update_status": "updateStatus",
            }

    @dataclass(frozen=True)
    class System(DataClassDictMixin):
        """System status."""

        country_code: str
        group_role: str
        hardware_id: str
        lan0_link: bool
        led_animation: str
        led_intensity: int
        model_id: str
        oobe_detailed_status: str
        uptime: int
        last_restart: datetime = field(init=False)

        class Config(BaseConfig):
            """Configure system serialization."""

            serialize_by_alias = True
            deserialize_by_alias = True
            aliases = {
                "country_code": "countryCode",
                "group_role": "groupRole",
                "hardware_id": "hardwareId",
                "lan0_link": "lan0Link",
                "led_animation": "ledAnimation",
                "led_intensity": "ledIntensity",
                "model_id": "modelId",
                "oobe_detailed_status": "oobeDetailedStatus",
            }

        def __post_init__(self) -> None:
            """Compute last_restart from uptime."""
            object.__setattr__(
                self,
                "last_restart",
                datetime.now() - timedelta(seconds=self.uptime),
            )

    @dataclass(frozen=True)
    class VorlonInfo(DataClassDictMixin):
        """Vorlon info status."""

        migration_mode: str

        class Config(BaseConfig):
            """Configure vorlon info serialization."""

            serialize_by_alias = True
            deserialize_by_alias = True
            aliases = {
                "migration_mode": "migrationMode",
            }

    @dataclass(frozen=True)
    class WAN(DataClassDictMixin):
        """WAN status."""

        captive_portal: bool
        ethernet_link: bool
        gateway_ip_address: IPAddress
        invalid_credentials: bool
        ip_address: bool
        ip_method: str
        ip_prefix_length: int
        lease_duration_seconds: int
        local_ip_address: IPAddress
        name_servers: list[IPAddress]
        online: bool
        pppoe_detected: bool
        vlan_scan_attempt_count: int
        vlan_scan_complete: bool

        class Config(BaseConfig):
            """Configure WAN serialization."""

            serialize_by_alias = True
            deserialize_by_alias = True
            aliases = {
                "captive_portal": "captivePortal",
                "ethernet_link": "ethernetLink",
                "gateway_ip_address": "gatewayIpAddress",
                "invalid_credentials": "invalidCredentials",
                "ip_address": "ipAddress",
                "ip_method": "ipMethod",
                "ip_prefix_length": "ipPrefixLength",
                "lease_duration_seconds": "leaseDurationSeconds",
                "local_ip_address": "localIpAddress",
                "name_servers": "nameServers",
                "pppoe_detected": "pppoeDetected",
                "vlan_scan_attempt_count": "vlanScanAttemptCount",
                "vlan_scan_complete": "vlanScanComplete",
            }
