"""Support for APPER Solaire PV Dimmer select entities."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


class PVDimmerSelectEntity(PVDimmerEntity, SelectEntity):
    """Representation of a select entity."""

    @property
    def options(self):
        """Get list of available options"""
        return list(self.entity_description.options_labels.values())

    @property
    def current_option(self):
        """Get currently selected option"""
        return self.entity_description.options_labels.get(self.native_value)

    async def async_select_option(self, value: str) -> None:
        """Update the current value."""
        real_value = list(self.entity_description.options_labels.keys())[
            list(self.entity_description.options_labels.values()).index(value)
        ]
        await self.coordinator.async_set_config(**{self.config_key: real_value})
        await self.coordinator.async_request_refresh()


@dataclass(frozen=True)
class PVDimmerSelectEntityDescription(PVDimmerEntityDescription, SelectEntityDescription):
    """Describes a APPER Solaire PV Dimmer's select entity."""

    object_class = PVDimmerSelectEntity
    options_labels: dict[str, Any] | None = None


ENTITIES: tuple[PVDimmerSelectEntityDescription, ...] = ()

STATE_ENTITIES: tuple[PVDimmerSelectEntityDescription, ...] = (
    PVDimmerSelectEntityDescription(
        key="config.delester",
        config_key="mode",
        unique_id_key="config_child_mode",
        name="Child mode",
        icon="mdi:ip-network",
        options_labels={"off": "Off", "delester": "Unload", "equal": "Equal"},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES, STATE_ENTITIES)
