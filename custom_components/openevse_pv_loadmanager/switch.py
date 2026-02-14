"""Switch platform for OpenEVSE PV Load Manager."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DEVICE_IDENTIFIER, DEVICE_INFO


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch entities from a config entry."""
    async_add_entities([
        EnableChargingSwitch(),
        LoadManagerModeSwitch(),
    ])


class EnableChargingSwitch(SwitchEntity, RestoreEntity):
    """Master switch to enable/disable charging.

    OFF = All charging disabled (default)
    ON = Load manager active
    """

    _attr_has_entity_name = True
    _attr_name = "Enable Charging"
    _attr_unique_id = f"{DEVICE_IDENTIFIER}_enable_charging"
    _attr_icon = "mdi:ev-station"
    _attr_device_info = DEVICE_INFO

    def __init__(self) -> None:
        self._attr_is_on = False  # Default: OFF

    async def async_added_to_hass(self) -> None:
        """Restore previous state on startup."""
        last_state = await self.async_get_last_state()
        if last_state is not None:
            self._attr_is_on = last_state.state == "on"

    async def async_turn_on(self, **kwargs) -> None:
        """Enable charging."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Disable charging."""
        self._attr_is_on = False
        self.async_write_ha_state()


class LoadManagerModeSwitch(SwitchEntity, RestoreEntity):
    """Switch to toggle between PV-Only and PV+Grid mode.

    ON = PV+Grid (full 32A available)
    OFF = PV-Only (only PV surplus)
    """

    _attr_has_entity_name = True
    _attr_name = "PV Load Manager Mode"
    _attr_unique_id = f"{DEVICE_IDENTIFIER}_mode"
    _attr_icon = "mdi:solar-power-variant"
    _attr_device_info = DEVICE_INFO

    def __init__(self) -> None:
        self._attr_is_on = True  # Default: PV+Grid

    async def async_added_to_hass(self) -> None:
        """Restore previous state on startup."""
        last_state = await self.async_get_last_state()
        if last_state is not None:
            self._attr_is_on = last_state.state == "on"

    async def async_turn_on(self, **kwargs) -> None:
        """Set PV+Grid mode."""
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Set PV-Only mode."""
        self._attr_is_on = False
        self.async_write_ha_state()
