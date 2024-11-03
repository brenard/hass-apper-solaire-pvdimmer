"""Config flow for APPER Solaire PV Dimmer integration."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import (
    CONF_DEFAULTS,
    CONF_HOST,
    CONF_INCLUDE_STATE_ENTITIES,
    CONF_REFRESH_RATE,
    CONF_TIMEOUT,
    DOMAIN,
)
from .helpers import async_request

_LOGGER = logging.getLogger(__name__)


class BaseConfigFlow:
    async def async_check_user_input(self, user_input: Mapping[str, Any] | None) -> str | None:
        """
        Check APPER Solaire PV Dimmer connection with user input
        Return APPER Solaire PV Dimmer name on success and set self._errors
        otherwise.
        """
        try:
            config = await async_request(
                async_create_clientsession(self.hass),
                f"http://{user_input[CONF_HOST]}/config",
            )
        except Exception as err:
            _LOGGER.warning("Failed to connect to APPER Solaire PV Dimmer: %s", err)
            self._errors["base"] = "cannot_connect"
            return False
        try:
            assert config["dimmername"]
            return config["dimmername"]
        except (KeyError, AssertionError):
            self._errors["base"] = "dimmer_name"
        return False

    @staticmethod
    def _get_config_schema(defaults=None):
        """Get configuration schema"""
        defaults = defaults or CONF_DEFAULTS
        return vol.Schema(
            {
                vol.Required(CONF_HOST, default=defaults.get(CONF_HOST)): str,
                vol.Required(
                    CONF_INCLUDE_STATE_ENTITIES, default=defaults.get(CONF_INCLUDE_STATE_ENTITIES)
                ): bool,
                vol.Required(CONF_REFRESH_RATE, default=defaults.get(CONF_REFRESH_RATE)): int,
                vol.Required(CONF_TIMEOUT, default=defaults.get(CONF_TIMEOUT)): int,
            }
        )


class ConfigFlow(BaseConfigFlow, config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for APPER Solaire PV Dimmer."""

    VERSION = 1

    async def async_step_user(self, user_input: Mapping[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        self._errors: dict[str, str] = {}
        if user_input:
            dimmer_name = await self.async_check_user_input(user_input)
            if dimmer_name and not self._errors:
                await self.async_set_unique_id(dimmer_name)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=dimmer_name, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=self._get_config_schema(), errors=self._errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlow(config_entry)


class OptionsFlow(BaseConfigFlow, config_entries.OptionsFlow):
    """Handle a options flow for APPER Solaire PV Dimmer."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Mapping[str, Any] | None = None) -> FlowResult:
        """Manage the options."""
        self._errors: dict[str, str] = {}
        if user_input:
            dimmer_name = await self.async_check_user_input(user_input)
            if dimmer_name and not self._errors:
                # update config entry
                self.hass.config_entries.async_update_entry(self.config_entry, data=user_input)
                # Finish
                return self.async_create_entry(data=None)

        return self.async_show_form(
            step_id="init",
            data_schema=self._get_config_schema(self.config_entry.data),
            errors=self._errors,
        )
