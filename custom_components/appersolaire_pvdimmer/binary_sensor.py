"""Support for APPER Solaire PV Dimmer binary sensors."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


class PVDimmerBinarySensorEntity(PVDimmerEntity, BinarySensorEntity):
    """Representation of a binary sensor entity."""

    @property
    def is_on(self):
        """Return current binary sensor state"""
        return bool(self.native_value)


@dataclass(frozen=True)
class PVDimmerBinarySensorEntityDescription(
    PVDimmerEntityDescription, BinarySensorEntityDescription
):
    """Describes a APPER Solaire PV Dimmer's binary sensor entity."""

    object_class = PVDimmerBinarySensorEntity


ENTITIES: tuple[PVDimmerBinarySensorEntityDescription, ...] = (
    PVDimmerBinarySensorEntityDescription(
        key="state.minuteur",
        unique_id_key="timer",
        name="Timer",
        icon="mdi:timer",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensor."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES)
