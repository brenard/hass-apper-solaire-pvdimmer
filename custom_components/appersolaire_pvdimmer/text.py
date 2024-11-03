"""Support for APPER Solaire PV Dimmer text entities."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.text import TextEntity, TextEntityDescription, TextMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


class PVDimmerTextEntity(PVDimmerEntity, TextEntity):
    """Representation of a text entity."""

    async def async_set_value(self, value: str) -> None:
        """Update the current value."""
        await self.coordinator.async_set_config(**{self.config_key: value})
        await self.coordinator.async_request_refresh()


@dataclass(frozen=True)
class PVDimmerTextEntityDescription(PVDimmerEntityDescription, TextEntityDescription):
    """Describes a APPER Solaire PV Dimmer's text entity."""

    object_class = PVDimmerTextEntity


ENTITIES: tuple[PVDimmerTextEntityDescription, ...] = (
    PVDimmerTextEntityDescription(
        key="config.child",
        unique_id_key="config_child_address",
        name="Child address",
        icon="mdi:ip-network",
    ),
    PVDimmerTextEntityDescription(
        key="config.dimmername",
        unique_id_key="config_hostname",
        name="Hostname",
        icon="mdi:form-textbox",
    ),
    PVDimmerTextEntityDescription(
        key="config.SubscribePV",
        unique_id_key="config_mqtt_dimmer_power_subscription",
        name="MQTT Dimmer power subscription",
        icon="mdi:form-textbox",
    ),
    PVDimmerTextEntityDescription(
        key="config.SubscribeTEMP",
        unique_id_key="config_mqtt_dimmer_temp_subscription",
        name="MQTT Dimmer temperature subscription",
        icon="mdi:form-textbox",
    ),
    PVDimmerTextEntityDescription(
        key="config.DALLAS",
        unique_id_key="config_master_dallas_address",
        name="Master DALLAS address",
        icon="mdi:form-textbox",
    ),
    PVDimmerTextEntityDescription(
        key="mqtt.server",
        config_key="hostname",
        unique_id_key="config_mqtt_server",
        name="MQTT Server",
        icon="mdi:ip-network",
    ),
    PVDimmerTextEntityDescription(
        key="mqtt.user",
        config_key="mqttuser",
        unique_id_key="config_mqtt_user",
        name="MQTT user",
        icon="mdi:shield-account",
    ),
    PVDimmerTextEntityDescription(
        key="mqtt.password",
        config_key="mqttpassword",
        unique_id_key="config_mqtt_password",
        name="MQTT password",
        icon="mdi:form-textbox-password",
        mode=TextMode.PASSWORD,
    ),
    PVDimmerTextEntityDescription(
        key="mqtt.topic",
        config_key="Publish",
        unique_id_key="config_mqtt_domoticz_topic",
        name="MQTT Domoticz topic",
        icon="mdi:form-textbox",
        cast_fn=lambda x: "No problem",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES)
