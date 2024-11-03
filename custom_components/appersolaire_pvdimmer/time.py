"""Support for APPER Solaire PV Dimmer time entities."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import time

from homeassistant.components.time import TimeEntity, TimeEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


class PVDimmerTimeEntity(PVDimmerEntity, TimeEntity):
    """Representation of a time entity."""

    @property
    def native_value(self):
        """Return current state."""
        value = super().native_value
        if value:
            parsed_value = value.split(":")
            assert len(parsed_value) == 2
            value = time(int(parsed_value[0]), int(parsed_value[1]))
        return value

    async def async_set_value(self, value: time) -> None:
        """Update the current value."""
        await self.coordinator.async_request(
            "setminuteur",
            params={
                self.entity_description.key.split("_", maxsplit=1)[0]: "",
                self.config_key: value.strftime("%H:%M"),
            },
        )
        await self.coordinator.async_request_refresh()


@dataclass(frozen=True)
class PVDimmerTimeEntityDescription(PVDimmerEntityDescription, TimeEntityDescription):
    """Describes a APPER Solaire PV Dimmer's time entity."""

    object_class = PVDimmerTimeEntity


ENTITIES: tuple[PVDimmerTimeEntityDescription, ...] = (
    # Timers configuration entities
    PVDimmerTimeEntityDescription(
        key="dimmer_timer.heure_demarrage",
        unique_id_key="config_dimmer_timer_start_hour",
        name="Dimmer timer start hour",
        icon="mdi:hours-24",
    ),
    PVDimmerTimeEntityDescription(
        key="dimmer_timer.heure_arret",
        unique_id_key="config_dimmer_timer_stop_hour",
        name="Dimmer timer stop hour",
        icon="mdi:hours-24",
    ),
    PVDimmerTimeEntityDescription(
        key="relay1_timer.heure_demarrage",
        unique_id_key="config_relay1_timer_start_hour",
        name="Relay 1 timer start hour",
        icon="mdi:hours-24",
    ),
    PVDimmerTimeEntityDescription(
        key="relay1_timer.heure_arret",
        unique_id_key="config_relay1_timer_stop_hour",
        name="Relay 1 timer stop hour",
        icon="mdi:hours-24",
    ),
    PVDimmerTimeEntityDescription(
        key="relay2_timer.heure_demarrage",
        unique_id_key="config_relay2_timer_start_hour",
        name="Relay 2 timer start hour",
        icon="mdi:hours-24",
    ),
    PVDimmerTimeEntityDescription(
        key="relay2_timer.heure_arret",
        unique_id_key="config_relay2_timer_stop_hour",
        name="Relay 2 timer stop hour",
        icon="mdi:hours-24",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES)
