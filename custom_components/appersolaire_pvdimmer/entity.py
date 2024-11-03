"""Parent Entity."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity import Entity, EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEFAULTS, CONF_HOST, CONF_INCLUDE_STATE_ENTITIES, DOMAIN, MANUFACTURER
from .coordinator import PVDimmerDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PVDimmerEntityDescription(EntityDescription):
    """Describes an entity."""

    object_class: PVDimmerEntity | None = None
    config_key: str | None = None
    unique_id_key: str | None = None
    value_fn: Callable[..., StateType] | None = None
    cast_fn: Callable[..., StateType] | None = None


class PVDimmerEntity(CoordinatorEntity[PVDimmerDataUpdateCoordinator], Entity):
    """Base class for all APPER Solaire PV Dimmer entities."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: PVDimmerDataUpdateCoordinator, description: EntityDescription
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = description

        self.dimmer_name = coordinator.dimmer_name
        if description.unique_id_key:
            self._attr_unique_id = f"{self.dimmer_name}_{description.unique_id_key}"
        else:
            self._attr_unique_id = f"{self.dimmer_name}_{description.key.replace('.', '_')}"
        self._attr_device_info = {
            "name": self.dimmer_name,
            "identifiers": {(DOMAIN, self.dimmer_name)},
            "manufacturer": MANUFACTURER,
            "configuration_url": f"http://{coordinator.config_entry.data[CONF_HOST]}",
        }
        if coordinator.dimmer_mac_address:
            self._attr_device_info["connections"] = {
                (device_registry.CONNECTION_NETWORK_MAC, coordinator.dimmer_mac_address)
            }

    @property
    def config_key(self):
        """Return configuration key"""
        return self.entity_description.config_key or self.entity_description.key.split(".")[-1]

    @property
    def native_value(self):
        """Return current state."""
        value = (
            self.entity_description.value_fn(self)
            if self.entity_description.value_fn is not None
            else self.coordinator.get_item(self.entity_description.key)
        )
        return (
            self.entity_description.cast_fn(value)
            if self.entity_description.cast_fn is not None and value is not None
            else value
        )


async def setup_platform_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
    entity_descriptions: tuple[PVDimmerEntityDescription, ...],
    state_entity_descriptions: tuple[PVDimmerEntityDescription, ...] | None = None,
) -> None:
    """Set up platform's entities."""
    coordinator = entry.runtime_data
    entities = [
        description.object_class(coordinator, description) for description in entity_descriptions
    ]
    if state_entity_descriptions and entry.data.get(
        CONF_INCLUDE_STATE_ENTITIES, CONF_DEFAULTS.get(CONF_INCLUDE_STATE_ENTITIES)
    ):
        entities.extend(
            [
                description.object_class(coordinator, description)
                for description in state_entity_descriptions
            ]
        )
    async_add_entities(entities)
