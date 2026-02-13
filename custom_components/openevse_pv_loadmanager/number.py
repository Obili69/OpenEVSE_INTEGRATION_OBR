"""Number platform for OpenEVSE PV Load Manager."""

from __future__ import annotations

from homeassistant.components import mqtt
from homeassistant.components.number import NumberEntity, NumberMode
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
    LM_TOPIC_CONFIG_HYSTERESIS,
    LM_TOPIC_CONFIG_HYSTERESIS_SET,
    LM_TOPIC_CONFIG_RAMP_DELAY,
    LM_TOPIC_CONFIG_RAMP_DELAY_SET,
)


def _device_info() -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, DEVICE_IDENTIFIER)},
        name=DEVICE_NAME,
        manufacturer=DEVICE_MANUFACTURER,
        model=DEVICE_MODEL,
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities from a config entry."""
    async_add_entities([
        HysteresisNumber(),
        RampDelayNumber(),
    ])


class HysteresisNumber(NumberEntity):
    """Number entity for hysteresis threshold (A)."""

    _attr_has_entity_name = True
    _attr_name = "Hysteresis Threshold"
    _attr_unique_id = f"{DEVICE_IDENTIFIER}_hysteresis"
    _attr_icon = "mdi:sine-wave"
    _attr_native_min_value = 0
    _attr_native_max_value = 10
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = "A"
    _attr_mode = NumberMode.SLIDER
    _attr_device_info = _device_info()

    def __init__(self) -> None:
        self._attr_native_value = 2.0

    async def async_added_to_hass(self) -> None:
        """Subscribe to hysteresis config topic."""

        @callback
        def message_received(msg):
            try:
                self._attr_native_value = float(msg.payload)
                self.async_write_ha_state()
            except (ValueError, TypeError):
                pass

        await mqtt.async_subscribe(
            self.hass, LM_TOPIC_CONFIG_HYSTERESIS, message_received, 0
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set new hysteresis threshold."""
        await mqtt.async_publish(
            self.hass, LM_TOPIC_CONFIG_HYSTERESIS_SET, str(value)
        )


class RampDelayNumber(NumberEntity):
    """Number entity for ramp-up delay (seconds)."""

    _attr_has_entity_name = True
    _attr_name = "Ramp-Up Delay"
    _attr_unique_id = f"{DEVICE_IDENTIFIER}_ramp_delay"
    _attr_icon = "mdi:timer-outline"
    _attr_native_min_value = 0
    _attr_native_max_value = 120
    _attr_native_step = 5
    _attr_native_unit_of_measurement = "s"
    _attr_mode = NumberMode.SLIDER
    _attr_device_info = _device_info()

    def __init__(self) -> None:
        self._attr_native_value = 30

    async def async_added_to_hass(self) -> None:
        """Subscribe to ramp delay config topic."""

        @callback
        def message_received(msg):
            try:
                self._attr_native_value = float(msg.payload)
                self.async_write_ha_state()
            except (ValueError, TypeError):
                pass

        await mqtt.async_subscribe(
            self.hass, LM_TOPIC_CONFIG_RAMP_DELAY, message_received, 0
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set new ramp-up delay."""
        await mqtt.async_publish(
            self.hass, LM_TOPIC_CONFIG_RAMP_DELAY_SET, str(value)
        )
