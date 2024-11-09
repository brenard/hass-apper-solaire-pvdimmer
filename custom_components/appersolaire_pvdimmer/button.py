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


class SaveConfigButton(PVDimmerEntity, ButtonEntity):
    """Representation of a button for saving configuration of APPER Solaire PV Dimmer to its flash memory."""

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_save_config()


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


class BackupButton(PVDimmerEntity, ButtonEntity):
    """Representation of a button for backuping APPER Solaire PV Dimmer configuration."""

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_backup_device()
        # Update entity state to update last_backup extra attribute
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        return {
            "last_backup": self.coordinator.last_backup,
        }


class RestoreButton(PVDimmerEntity, ButtonEntity):
    """Representation of a button for restoring APPER Solaire PV Dimmer configuration."""

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_restore_device()


ENTITIES: tuple[PVDimmerButtonEntityDescription, ...] = (
    PVDimmerButtonEntityDescription(
        object_class=SaveConfigButton,
        key="save_config",
        name="Save configuration",
        icon="mdi:content-save-settings",
    ),
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
    PVDimmerButtonEntityDescription(
        object_class=BackupButton,
        key="backup_config",
        name="Backup configuration",
        icon="mdi:briefcase-download",
    ),
    PVDimmerButtonEntityDescription(
        object_class=RestoreButton,
        key="restore_config",
        name="Restore configuration",
        icon="mdi:briefcase-upload",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES)
