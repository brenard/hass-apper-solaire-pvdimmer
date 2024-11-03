"""Button for APPER Solaire PV Dimmer."""

import logging
from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PVDimmerButtonEntityDescription(PVDimmerEntityDescription, ButtonEntityDescription):
    """Describes a APPER Solaire PV Dimmer's button entity."""


class RestartButton(PVDimmerEntity, ButtonEntity):
    """Representation of a button for reboot APPER Solaire PV Dimmer."""

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_request("reset", json_decode=False)


class RefreshButton(PVDimmerEntity, ButtonEntity):
    """Representation of a button for refreshing integration data."""

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_request_refresh()


class ResetWifiSettingButton(PVDimmerEntity, ButtonEntity):
    """Representation of a button for resetting APPER Solaire PV Dimmer WIFI setting."""

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_request("resetwifi", json_decode=False)


ENTITIES: tuple[PVDimmerButtonEntityDescription, ...] = (
    PVDimmerButtonEntityDescription(
        object_class=RestartButton, key="restart", name="Restart", icon="mdi:restart-alert"
    ),
    PVDimmerButtonEntityDescription(
        object_class=RefreshButton, key="refresh", name="Refresh", icon="mdi:refresh-circle"
    ),
    PVDimmerButtonEntityDescription(
        object_class=ResetWifiSettingButton,
        key="resetwifi",
        name="Reset WIFI settings",
        icon="mdi:wifi-cog",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES)
