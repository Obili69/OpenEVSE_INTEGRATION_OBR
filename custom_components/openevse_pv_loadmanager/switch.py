"""Switch platform for OpenEVSE PV Load Manager."""

from __future__ import annotations

from homeassistant.components import mqtt
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DEVICE_IDENTIFIER,
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    DEVICE_NAME,
    DOMAIN,
    LM_TOPIC_MODE,
    LM_TOPIC_MODE_SET,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch entities from a config entry."""
    async_add_entities([LoadManagerModeSwitch()])


class LoadManagerModeSwitch(SwitchEntity):
    """Switch to toggle between PV-Only and PV+Grid mode.

    ON = PV+Grid (full 32A available)
    OFF = PV-Only (only PV surplus)
    """

    _attr_has_entity_name = True
    _attr_name = "PV Load Manager Mode"
    _attr_unique_id = f"{DEVICE_IDENTIFIER}_mode"
    _attr_icon = "mdi:solar-power-variant"
    _attr_device_info = DeviceInfo(
        identifiers={(DOMAIN, DEVICE_IDENTIFIER)},
        name=DEVICE_NAME,
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
    )

    def __init__(self) -> None:
        self._attr_is_on = True  # Default: PV+Grid

    async def async_added_to_hass(self) -> None:
        """Subscribe to mode topic when added to HA."""

        @callback
        def message_received(msg):
            payload = msg.payload.strip().lower()
            self._attr_is_on = payload == "pv_plus_grid"
            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, LM_TOPIC_MODE, message_received, 0)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on: set PV+Grid mode."""
        await mqtt.async_publish(self.hass, LM_TOPIC_MODE_SET, "pv_plus_grid")

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off: set PV-Only mode."""
        await mqtt.async_publish(self.hass, LM_TOPIC_MODE_SET, "pv_only")
