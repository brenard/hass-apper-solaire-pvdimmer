"""The APPER Solaire PV Dimmer integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import PVDimmerDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.TEXT,
    Platform.TIME,
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry[PVDimmerDataUpdateCoordinator]
) -> bool:
    """Set up APPER Solaire PV Dimmer from a config entry."""
    coordinator = PVDimmerDataUpdateCoordinator(hass, entry)
    entry.async_on_unload(entry.add_update_listener(coordinator.update_configuration))
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ConfigEntry[PVDimmerDataUpdateCoordinator]
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
