"""Button for APPER Solaire PV Dimmer router."""

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import PVDimmerDataUpdateCoordinator
from .entity import PVDimmerEntity, PVDimmerEntityDescription, setup_platform_entry

_LOGGER = logging.getLogger(__name__)


class PVDimmerSwitchEntity(PVDimmerEntity, SwitchEntity):
    """Representation of a switch entity."""

    @property
    def is_on(self) -> bool:
        """Return true if switch is currently enabled."""
        return bool(self.native_value)

    async def async_set_state(self, state: bool) -> None:
        """Turn the switch on."""
        await self.coordinator.async_request(
            self.entity_description.set_request_path,
            params=self.entity_description.set_request_compute_args(self, state),
        )
        if self.entity_description.waiting_delay_after_toggle:
            _LOGGER.debug(
                "Request sent, we need to wait a bit (%ds) before updating state...",
                self.entity_description.waiting_delay_after_toggle,
            )
            await asyncio.sleep(self.entity_description.waiting_delay_after_toggle)
        _LOGGER.debug("Updating state")
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        await self.async_set_state(True)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        await self.async_set_state(False)


@dataclass(frozen=True)
class PVDimmerSwitchEntityDescription(PVDimmerEntityDescription, SwitchEntityDescription):
    """Describes a APPER Solaire PV Dimmer's switch entity."""

    object_class = PVDimmerSwitchEntity
    options_labels: dict[str, Any] | None = None
    set_request_path: str | None = "get"
    set_request_compute_args: Callable[[PVDimmerSwitchEntity, bool], None] = lambda self, state: {
        self.config_key: int(state)
    }  # noqa: E731
    waiting_delay_after_toggle: int | None = None

    icon = ("mdi:toggle-switch-variant-off",)
    device_class = SwitchDeviceClass.SWITCH


ENTITIES: tuple[PVDimmerSwitchEntityDescription, ...] = ()

STATE_ENTITIES: tuple[PVDimmerSwitchEntityDescription, ...] = (
    PVDimmerSwitchEntityDescription(
        key="state.onoff",
        config_key="dimmer_on_off",
        unique_id_key="dimmer",
        name="Dimmer",
    ),
    PVDimmerSwitchEntityDescription(
        key="state.relay1",
        config_key="relay1",
        unique_id_key="relay1",
        name="Relay 1",
    ),
    PVDimmerSwitchEntityDescription(
        key="state.relay2",
        config_key="relay2",
        unique_id_key="relay2",
        name="Relay 2",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PVDimmerDataUpdateCoordinator],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entities."""
    await setup_platform_entry(hass, entry, async_add_entities, ENTITIES, STATE_ENTITIES)
