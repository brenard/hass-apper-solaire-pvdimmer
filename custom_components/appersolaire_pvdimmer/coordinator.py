"""Coordinator for APPER Solaire PV Dimmer."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from scapy.layers.l2 import getmacbyip

from .const import CONF_DEFAULTS, CONF_HOST, CONF_REFRESH_RATE, CONF_TIMEOUT, DOMAIN
from .helpers import async_request

_LOGGER = logging.getLogger(__name__)


class PVDimmerDataUpdateCoordinator(DataUpdateCoordinator):
    """Define an object to fetch data."""

    _dimmer_mac_address = None

    def __init__(
        self,
        hass: HomeAssistant,
        entry,
    ) -> None:
        """Class to manage fetching data API."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=entry.data.get(CONF_REFRESH_RATE, CONF_DEFAULTS[CONF_REFRESH_RATE])
            ),
        )
        self.entry = entry
        self._session = async_create_clientsession(self.hass)

    async def async_request(self, path: str, **kwargs: Any) -> Any:
        """Request url with method."""
        return await async_request(
            self._session,
            f"http://{self.dimmer_ip}/{path}",
            timeout=self.entry.data.get(CONF_TIMEOUT, CONF_DEFAULTS[CONF_TIMEOUT]),
            **kwargs,
        )

    async def update_configuration(self, hass, entry):
        """Update configuration"""
        self.entry = entry

        # Reset APPER Solaire PV Dimmer MAC address cache
        self._dimmer_mac_address = None

        self.update_interval = timedelta(seconds=entry.data[CONF_REFRESH_RATE])
        _LOGGER.debug("Coordinator refresh interval updated (%s)", self.update_interval)

        _LOGGER.debug("Force update")
        await self.async_refresh()

    async def async_get_data(self) -> dict[str, dict[str, Any]]:
        """Fetch data."""
        return {
            "state": await self.async_request("state"),
            "config": await self.async_request("config"),
            "mqtt": await self.async_request("getmqtt"),
            "dimmer_timer": await self.async_request("getminuteur?dimmer"),
            "relay1_timer": await self.async_request("getminuteur?relay1"),
            "relay2_timer": await self.async_request("getminuteur?relay2"),
        }

    async def async_set_config(self, **kwargs):
        """Set APPER Solaire PV Dimmer config keys"""
        return await self.async_request("get", params=kwargs)

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Fetch data."""
        try:
            data = await self.async_get_data()
        except Exception as error:
            _LOGGER.error(error)
            raise UpdateFailed from error

        return data

    def get_item(self, key_chain: str, default: Any = None) -> Any:
        """
        Get recursive key and return value.

        :param key: The excepted item key chain (with dot for key delimited, ex: "key.key.key")
        """
        data = self.data
        if (keys := key_chain.split(".")) and isinstance(keys, list):
            for key in keys:
                if isinstance(data, dict):
                    data = data.get(key)
        return default if data is None and default is not None else data

    @property
    def dimmer_ip(self):
        """Get APPER Solaire PV Dimmer IP address"""
        return self.entry.data[CONF_HOST]

    @property
    def dimmer_name(self):
        """Get APPER Solaire PV Dimmer name"""
        return self.get_item("config.dimmername")

    @property
    def dimmer_mac_address(self):
        """Get APPER Solaire PV Dimmer MAC address"""
        if not self._dimmer_mac_address:
            self._dimmer_mac_address = getmacbyip(self.entry.data[CONF_HOST])
        return self._dimmer_mac_address
