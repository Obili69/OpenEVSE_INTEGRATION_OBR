"""Sensor platform for OpenEVSE PV Load Manager."""

from __future__ import annotations

from homeassistant.components import mqtt
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_NUM_STATIONS,
    DEVICE_IDENTIFIER,
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    DEVICE_NAME,
    DOMAIN,
    LM_TOPIC_EVSE_ACTUAL,
    LM_TOPIC_EVSE_ENERGY,
    LM_TOPIC_EVSE_SETPOINT,
    LM_TOPIC_EVSE_STATE,
    LM_TOPIC_STATUS,
    LM_TOPIC_TOTAL_ALLOCATED,
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
    """Set up sensor entities from a config entry."""
    num_stations = hass.data[DOMAIN][entry.entry_id][CONF_NUM_STATIONS]
    entities: list[SensorEntity] = []

    # Global sensors
    entities.append(
        MQTTSensor(
            name="Load Manager Status",
            unique_id=f"{DEVICE_IDENTIFIER}_status",
            topic=LM_TOPIC_STATUS,
            icon="mdi:information-outline",
        )
    )
    entities.append(
        MQTTSensor(
            name="Total Allocated Current",
            unique_id=f"{DEVICE_IDENTIFIER}_total_allocated",
            topic=LM_TOPIC_TOTAL_ALLOCATED,
            unit="A",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:current-ac",
        )
    )

    # Per-station sensors
    for sid in range(1, num_stations + 1):
        entities.extend([
            MQTTSensor(
                name=f"EVSE {sid} Setpoint",
                unique_id=f"{DEVICE_IDENTIFIER}_evse{sid}_setpoint",
                topic=LM_TOPIC_EVSE_SETPOINT.format(sid),
                unit="A",
                device_class=SensorDeviceClass.CURRENT,
                state_class=SensorStateClass.MEASUREMENT,
                icon="mdi:flash",
            ),
            MQTTSensor(
                name=f"EVSE {sid} Actual Current",
                unique_id=f"{DEVICE_IDENTIFIER}_evse{sid}_actual",
                topic=LM_TOPIC_EVSE_ACTUAL.format(sid),
                unit="A",
                device_class=SensorDeviceClass.CURRENT,
                state_class=SensorStateClass.MEASUREMENT,
                icon="mdi:flash",
            ),
            MQTTSensor(
                name=f"EVSE {sid} State",
                unique_id=f"{DEVICE_IDENTIFIER}_evse{sid}_state",
                topic=LM_TOPIC_EVSE_STATE.format(sid),
                icon="mdi:ev-station",
            ),
            MQTTSensor(
                name=f"EVSE {sid} Session Energy",
                unique_id=f"{DEVICE_IDENTIFIER}_evse{sid}_energy",
                topic=LM_TOPIC_EVSE_ENERGY.format(sid),
                unit="kWh",
                device_class=SensorDeviceClass.ENERGY,
                state_class=SensorStateClass.TOTAL_INCREASING,
                icon="mdi:battery-charging",
            ),
        ])

    async_add_entities(entities)


class MQTTSensor(SensorEntity):
    """A sensor entity that gets its value from an MQTT topic."""

    _attr_has_entity_name = True

    def __init__(
        self,
        name: str,
        unique_id: str,
        topic: str,
        unit: str | None = None,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
        icon: str | None = None,
    ) -> None:
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._topic = topic
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_icon = icon
        self._attr_device_info = _device_info()

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT topic when added to HA."""

        @callback
        def message_received(msg):
            """Handle new MQTT message."""
            payload = msg.payload
            if self._attr_device_class in (
                SensorDeviceClass.CURRENT,
                SensorDeviceClass.ENERGY,
            ):
                try:
                    self._attr_native_value = float(payload)
                except (ValueError, TypeError):
                    self._attr_native_value = None
            else:
                self._attr_native_value = payload
            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic, message_received, 0)
