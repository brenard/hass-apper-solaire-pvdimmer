"""Support for APPER Solaire PV Dimmer number entities."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberEntityDescription
from homeassistant.components.number.const import NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


class PVDimmerNumberEntity(PVDimmerEntity, NumberEntity):
    """Representation of a number entity."""

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self.coordinator.async_set_config(**{self.config_key: int(value)})
        await self.coordinator.async_request_refresh()


class PVDimmerPowerNumberEntity(PVDimmerEntity, NumberEntity):
    """Representation of a number entity to control power."""

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self.coordinator.async_request("", params={"POWER": value})
        await self.coordinator.async_request_refresh()


class PVDimmerTimerNumberEntity(PVDimmerEntity, NumberEntity):
    """Representation of a number entity for timer."""

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        await self.coordinator.async_request(
            "setminuteur",
            params={
                self.entity_description.key.split("_", maxsplit=1)[0]: "",
                self.config_key: int(value),
            },
        )
        await self.coordinator.async_request_refresh()


@dataclass(frozen=True)
class PVDimmerNumberEntityDescription(PVDimmerEntityDescription, NumberEntityDescription):
    """Describes a APPER Solaire PV Dimmer's number entity."""

    object_class = PVDimmerNumberEntity


ENTITIES: tuple[PVDimmerNumberEntityDescription, ...] = (
    # General configuration entities
    PVDimmerNumberEntityDescription(
        key="config.trigger",
        name="Trigger",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:percent",
    ),
    PVDimmerNumberEntityDescription(
        key="config.charge1",
        unique_id_key="config_load1",
        name="Load 1 (Dimmer)",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        native_step=1,
        native_max_value=10000,
        mode=NumberMode.BOX,
        icon="mdi:meter-electric",
    ),
    PVDimmerNumberEntityDescription(
        key="config.charge2",
        unique_id_key="config_load2",
        name="Load 2 (Jotta)",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        native_step=1,
        native_max_value=10000,
        mode=NumberMode.BOX,
        icon="mdi:meter-electric",
    ),
    PVDimmerNumberEntityDescription(
        key="config.charge3",
        unique_id_key="config_load3",
        name="Load 3 (relay 2)",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        native_step=1,
        native_max_value=10000,
        mode=NumberMode.BOX,
        icon="mdi:meter-electric",
    ),
    # MQTT configuration entities
    PVDimmerNumberEntityDescription(
        key="mqtt.port",
        unique_id_key="config_mqtt_port",
        name="MQTT port",
        native_step=1,
        native_min_value=1,
        native_max_value=65535,
        mode=NumberMode.BOX,
        icon="mdi:network",
    ),
    PVDimmerNumberEntityDescription(
        key="mqtt.idxtemp",
        unique_id_key="config_mqtt_domoticz_idx_temperature",
        name="MQTT Domoticz IDX temperature",
        native_step=1,
        native_min_value=1,
        native_max_value=65535,
        mode=NumberMode.BOX,
        icon="mdi:numeric",
    ),
    PVDimmerNumberEntityDescription(
        key="mqtt.IDX",
        unique_id_key="config_mqtt_domoticz_idx_power",
        name="MQTT Domoticz IDX power",
        native_step=1,
        native_min_value=1,
        native_max_value=65535,
        mode=NumberMode.BOX,
        icon="mdi:numeric",
    ),
    PVDimmerNumberEntityDescription(
        key="mqtt.IDXAlarme",
        unique_id_key="config_mqtt_domoticz_idx_alarm",
        name="MQTT Domoticz IDX alarm",
        native_step=1,
        native_min_value=1,
        native_max_value=65535,
        mode=NumberMode.BOX,
        icon="mdi:numeric",
    ),
    # Timers configuration entities
    PVDimmerNumberEntityDescription(
        object_class=PVDimmerTimerNumberEntity,
        key="dimmer_timer.temperature",
        unique_id_key="config_dimmer_timer_temperature",
        name="Dimmer timer temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_step=1,
        native_min_value=0,
        native_max_value=100,
        device_class=NumberDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
        mode=NumberMode.BOX,
    ),
    PVDimmerNumberEntityDescription(
        object_class=PVDimmerTimerNumberEntity,
        key="relay1_timer.temperature",
        unique_id_key="config_relay1_timer_temperature",
        name="Relay 1 timer temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_step=1,
        native_min_value=0,
        native_max_value=100,
        device_class=NumberDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
        mode=NumberMode.BOX,
    ),
    PVDimmerNumberEntityDescription(
        object_class=PVDimmerTimerNumberEntity,
        key="relay2_timer.temperature",
        unique_id_key="config_relay2_timer_temperature",
        name="Relay 2 timer temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        native_step=1,
        native_min_value=0,
        native_max_value=100,
        device_class=NumberDeviceClass.TEMPERATURE,
        icon="mdi:thermometer",
        mode=NumberMode.BOX,
    ),
    PVDimmerNumberEntityDescription(
        object_class=PVDimmerTimerNumberEntity,
        key="dimmer_timer.puissance",
        unique_id_key="config_dimmer_timer_puissance",
        name="Dimmer timer puissance",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:percent",
    ),
    PVDimmerNumberEntityDescription(
        object_class=PVDimmerTimerNumberEntity,
        key="relay1_timer.puissance",
        unique_id_key="config_relay1_timer_puissance",
        name="Relay 1 timer puissance",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:percent",
    ),
    PVDimmerNumberEntityDescription(
        object_class=PVDimmerTimerNumberEntity,
        key="relay2_timer.puissance",
        unique_id_key="config_relay2_timer_puissance",
        name="Relay 2 timer puissance",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:percent",
    ),
)

STATE_ENTITIES: tuple[PVDimmerNumberEntityDescription, ...] = (
    PVDimmerNumberEntityDescription(
        key="state.power",
        unique_id_key="power",
        name="Power",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        mode=NumberMode.AUTO,
        icon="mdi:percent",
        cast_fn=float,
        object_class=PVDimmerPowerNumberEntity,
    ),
    PVDimmerNumberEntityDescription(
        key="config.startingpow",
        unique_id_key="config_mqtt_dimmer_start_power",
        name="MQTT Dimmer starting power",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        native_max_value=None,
        mode=NumberMode.BOX,
        icon="mdi:percent",
    ),
    PVDimmerNumberEntityDescription(
        key="config.minpow",
        unique_id_key="config_minpower",
        name="Min power",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:percent",
    ),
    PVDimmerNumberEntityDescription(
        key="config.maxpow",
        unique_id_key="config_maxpower",
        name="Max power",
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.POWER_FACTOR,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:percent",
    ),
    PVDimmerNumberEntityDescription(
        key="config.maxtemp",
        name="Max temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=NumberDeviceClass.TEMPERATURE,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:thermometer",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES, STATE_ENTITIES)
