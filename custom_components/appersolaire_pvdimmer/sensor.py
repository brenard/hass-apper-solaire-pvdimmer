"""Support for APPER Solaire PV Dimmer sensors."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


class PVDimmerSensorEntity(PVDimmerEntity, SensorEntity):
    """Representation of a sensor entity."""


@dataclass(frozen=True)
class PVDimmerSensorEntityDescription(PVDimmerEntityDescription, SensorEntityDescription):
    """Describes a APPER Solaire PV Dimmer's sensor entity."""

    object_class = PVDimmerSensorEntity


ENTITIES: tuple[PVDimmerSensorEntityDescription, ...] = ()

STATE_ENTITIES: tuple[PVDimmerSensorEntityDescription, ...] = (
    PVDimmerSensorEntityDescription(
        key="state.temperature",
        unique_id_key="temperature",
        name="Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        cast_fn=float,
    ),
    PVDimmerSensorEntityDescription(
        key="state.power",
        unique_id_key="power",
        name="Power",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.POWER_FACTOR,
        icon="mdi:percent",
        state_class=SensorStateClass.MEASUREMENT,
        cast_fn=float,
    ),
    PVDimmerSensorEntityDescription(
        key="state.Ptotal",
        unique_id_key="total_power",
        name="Total power",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.POWER_FACTOR,
        icon="mdi:percent",
        state_class=SensorStateClass.MEASUREMENT,
        cast_fn=float,
    ),
    PVDimmerSensorEntityDescription(
        key="state.alerte",
        unique_id_key="warning",
        name="Warning",
        icon="mdi:alert-circle",
        cast_fn=lambda x: x if x else "No problem",
    ),
    PVDimmerSensorEntityDescription(
        key="last_backup",
        name="Last backup",
        icon="mdi:archive-clock-outline",
        value_fn=lambda self: self.coordinator.last_backup,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES, STATE_ENTITIES)
