"""Coordinator for APPER Solaire PV Dimmer."""

from __future__ import annotations

import json
import logging
import os.path
from datetime import datetime, timedelta
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
        self._backup_path = os.path.join(
            hass.config.path(),
            "_".join([DOMAIN, self.dimmer_mac_address.replace(":", ""), "config.json"]),
        )
        self._last_backup = None

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

    async def async_save_config(self):
        """Save APPER Solaire PV Dimmer configuration to its flash memory"""
        return await self.async_request("get", params={"save": "yes"})

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Fetch data."""
        if not self._last_backup and os.path.exists(self._backup_path):
            await self.hass.async_add_executor_job(self._load_backup)
        try:
            data = await self.async_get_data()
        except Exception as error:
            _LOGGER.error(error)
            raise UpdateFailed from error

        return data

    def get_item(
        self, key_chain: str, default: Any = None, data: dict[str, Any] | None = None
    ) -> Any:
        """
        Get recursive key and return value.

        :param key: The excepted item key chain (with dot for key delimited, ex: "key.key.key")
        """
        data = data or self.data
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

    #
    # Backup/restore configuration stuff
    #

    def _load_backup(self):
        """
        Load configuration backup and store it in self._last_backup

        Note: need to be run using hass.async_add_executor_job() helper since its contain
        I/O locking calls.
        """
        _LOGGER.debug("Load last backup from %s", self._backup_path)
        try:
            with open(self._backup_path, encoding="utf8") as fd:
                self._last_backup = json.load(fd)
                self._last_backup["time"] = datetime.fromisoformat(self._last_backup["time"])
        except (OSError, ValueError):
            _LOGGER.exception("Failed to load last backup from %s", self._backup_path)
            self._last_backup = None
        self.update_last_backup_sensor_entity_state()

    def _save_backup(self, data):
        """
        Save configuration backup

        Note: need to be run using hass.async_add_executor_job() helper since its contain
        I/O locking calls.
        """
        try:
            with open(self._backup_path, "w", encoding="utf8") as fd:
                json.dump(
                    data, fd, default=lambda x: x.isoformat() if isinstance(x, datetime) else x
                )
            _LOGGER.debug("PV dimmer configuration backup in %s", self._backup_path)
        except Exception:
            _LOGGER.exception("Failed to backup configuration in %s", self._backup_path)
            if os.path.exists(self._backup_path):
                os.remove(self._backup_path)

    async def async_backup_device(self):
        """Backup PV dimmer configuration"""
        data = {
            "data": await self.async_get_data(),
            "time": datetime.now(),
        }
        await self.hass.async_add_executor_job(self._save_backup, data)
        self._last_backup = data
        self.update_last_backup_sensor_entity_state()

    def update_last_backup_sensor_entity_state(self):
        """Update last_backup sensor entity state"""
        for update_callback, _ in list(self._listeners.values()):
            if "last_backup" in update_callback.__self__.unique_id:
                update_callback()

    async def async_restore_device(self):
        """Restore PV dimmer configuration"""
        assert self._last_backup, "No available backup to restore"
        _LOGGER.debug(
            "Restore PV dimmer configuration from last backup (%s): %s",
            self._last_backup["time"],
            self._last_backup["data"],
        )

        restore_calls = [
            {
                "title": "General configuration",
                "path": "get",
                "data": {
                    "maxtemp": "config.maxtemp",
                    "startingpow": "config.startingpow",
                    "minpow": "config.minpow",
                    "maxpow": "config.maxpow",
                    "child": "config.child",
                    "SubscribePV": "config.SubscribePV",
                    "SubscribeTEMP": "config.SubscribeTEMP",
                    "mode": "config.delester",
                    "charge1": "config.charge1",
                    "charge2": "config.charge2",
                    "charge3": "config.charge3",
                    "DALLAS": "config.DALLAS",
                    "dimmername": "config.dimmername",
                    "trigger": "config.trigger",
                },
            },
            {
                "title": "MQTT configuration",
                "path": "get",
                "data": {
                    "hostname": "mqtt.server",
                    "port": "mqtt.port",
                    "Publish": "mqtt.topic",
                    "mqttuser": "mqtt.user",
                    "mqttpassword": "mqtt.password",
                    "idxtemp": "mqtt.idxtemp",
                    "IDXAlarme": "mqtt.IDXAlarme",
                    "IDX": "mqtt.IDX",
                },
            },
            {
                "title": "Dimmer timer configuration",
                "path": "setminuteur",
                "params": {
                    "dimmer": "",
                },
                "data": {
                    "heure_demarrage": "dimmer_timer.heure_demarrage",
                    "heure_arret": "dimmer_timer.heure_arret",
                    "temperature": "dimmer_timer.temperature",
                    "puissance": "dimmer_timer.puissance",
                },
            },
            {
                "title": "Relay 1 timer configuration",
                "path": "setminuteur",
                "params": {
                    "relay1": "",
                },
                "data": {
                    "heure_demarrage": "relay1_timer.heure_demarrage",
                    "heure_arret": "relay1_timer.heure_arret",
                    "temperature": "relay1_timer.temperature",
                    "puissance": "relay1_timer.puissance",
                },
            },
            {
                "title": "Relay 2 timer configuration",
                "path": "setminuteur",
                "params": {
                    "relay2": "",
                },
                "data": {
                    "heure_demarrage": "relay2_timer.heure_demarrage",
                    "heure_arret": "relay2_timer.heure_arret",
                    "temperature": "relay2_timer.temperature",
                    "puissance": "relay2_timer.puissance",
                },
            },
        ]

        for call in restore_calls:
            params = call.get("params", {})
            for dst, src in call["data"].items():
                value = self.get_item(src, None, self._last_backup["data"])
                if value is not None:
                    params[dst] = value

            if not params:
                _LOGGER.warning("No %s to restore", call["title"])
                continue
            _LOGGER.debug("Restoring %s...", call["title"])
            await self.async_request(call["path"], params=params)
            _LOGGER.debug("%s restored", call["title"])
        await self.async_save_config()

    @property
    def last_backup(self):
        """Return last device backup time"""
        return self._last_backup["time"] if self._last_backup else None
