"""Constants for the OpenEVSE PV Load Manager integration."""

from homeassistant.helpers.device_registry import DeviceInfo

DOMAIN = "openevse_pv_loadmanager"

# Config keys
CONF_NUM_STATIONS = "num_stations"

# Device info
DEVICE_IDENTIFIER = "openevse_pv_loadmanager"
DEVICE_NAME = "OpenEVSE PV Load Manager"
DEVICE_MANUFACTURER = "Custom"
DEVICE_MODEL = "PV Load Manager v2.0"

DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, DEVICE_IDENTIFIER)},
    name=DEVICE_NAME,
    manufacturer=DEVICE_MANUFACTURER,
    model=DEVICE_MODEL,
)
